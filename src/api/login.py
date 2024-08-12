from fastapi import APIRouter, HTTPException, Response, Cookie, Request, BackgroundTasks
from api.model import (
    LoginRequest,
    LoginResponse,
    ResetPasswordRequest,
    ConfirmEmailCodeRequest,
)
from crud.user import get_user_identifier, get_public_user, change_pswd
from crud.sessions import create_login_session, delete_session, clear_sessions_for_user
import bcrypt
import pyotp
import json
from tools import (
    SessionConfig,
    r,
    SecurityConfig,
    send_email,
    all_ids,
    regenerate_ids,
    SignupConfig,
    AccountFeaturesConfig,
)

router = APIRouter(
    prefix="",
    tags=["Log In"],
)


@router.post(
    "/forgot-password",
    status_code=204,
    responses={
        204: {"description": "Password Reset Email Sent"},
        403: {"description": "Resetting Password is disabled."},
        409: {
            "description": "Password Reset Email already sent. You have one request pending."
        },
        200: {"description": "Password Reset Successfully"},
    },
)
async def forgot_password(
    password_reset_form: ResetPasswordRequest, background_tasks: BackgroundTasks
):
    """
    # Reset Password

    ## Description
    This endpoint is used to reset the password of the user.
    """
    user = get_user_identifier(password_reset_form.identifier)
    public_user = get_public_user(user["_id"])
    if not AccountFeaturesConfig.enable_reset_pswd:
        raise HTTPException(status_code=403, detail="Resetting Password is disabled.")

    # Send Confirmation E-Mail
    if r.get("reset_pswd:" + user["email"]):
        raise HTTPException(
            status_code=409,
            detail="Password Reset Email already sent. You have one request pending.",
        )
    if not all_ids:
        # Generate new ids
        regenerate_ids()
    # Get a unique ID for confirmation email
    unique_id = all_ids.pop()
    r.setex(
        "reset_pswd:" + user["email"],
        SignupConfig.conf_code_expiry * 60,
        json.dumps(
            {
                "action": "password_reset",
                "code": unique_id,
                "new_pswd": password_reset_form.password,
            }
        ),
    )
    background_tasks.add_task(
        send_email,
        "ChangePassword",
        user["email"],
        code=unique_id,
        time=SignupConfig.conf_code_expiry,
        **public_user,
    )
    return Response(status_code=204)


@router.post(
    "/confirm-password",
    status_code=204,
    responses={
        204: {"description": "Password Reset Successfully"},
        403: {"description": "Resetting Password is disabled."},
        404: {"description": "No Password Reset Request found."},
        401: {"description": "Invalid Code"},
    },
)
async def confirm_reset(code: ConfirmEmailCodeRequest):
    """
    # Confirm Password Reset

    ## Description
    This endpoint is used to confirm a password reset.
    """
    user = get_user_identifier(code.identifier)
    if not AccountFeaturesConfig.enable_reset_pswd:
        raise HTTPException(status_code=403, detail="Resetting Password is disabled.")
    change_req = r.get("reset_pswd:" + user["email"])
    if not change_req:
        raise HTTPException(status_code=404, detail="No Password Reset Request found.")
    change_req = json.loads(change_req)
    # Check code
    if str(change_req["code"]) != str(code.code):
        raise HTTPException(status_code=401, detail="Invalid Code")

    change_pswd(user["_id"], change_req["new_pswd"])
    r.delete("reset_pswd:" + user["email"])

    # Delete all sessions
    clear_sessions_for_user(user["_id"])


@router.post(
    "/login",
    status_code=200,
    responses={
        401: {"description": "Invalid Credentials"},
        404: {"description": "User not found"},
        406: {"description": "2FA Required"},
    },
    response_model=LoginResponse,
)
async def login(login_form: LoginRequest, response: Response, request: Request):
    """
    # Log In (Create Session)

    ## Description
    This endpoint is used to log in a user and create a session.
    Returns a session token if the credentials are correct.
    Can also return a `Set-Cookie` header with the session token. (See Config)
    """
    user = get_user_identifier(login_form.identifier)
    # Check if User can be found
    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    # Check if Password Exists (or if OAuth SignIn)
    if not user.get("password", None):
        raise HTTPException(
            detail="You created your Account with OAuth. Please Reset your Password once logged in.",
            status_code=406,
        )

    uid_email_key = "invallogin:" + user["email"]

    # Get Failed Attempts from Redis
    failed_attempts = r.get(uid_email_key)
    # Max Login Attempts enabled? and already failed attempts? and reached max?
    if (
        SecurityConfig.max_login_attempts > 0
        and failed_attempts
        and int(failed_attempts) >= SecurityConfig.max_login_attempts
    ):
        # Set expiry for the failed attempts
        # If the user logs in successfully, this key will be deleted
        r.expire(uid_email_key, SecurityConfig.login_timeout * 60)
        raise HTTPException(
            detail="Too many failed login attempts. Please try again later.",
            status_code=429,
        )
    # Check Password
    if not bcrypt.checkpw(
        login_form.password.get_secret_value().encode("utf-8"),
        user["password"].encode("utf-8"),
    ):
        # Wrong Password
        if SecurityConfig.max_login_attempts > 0:
            r.incrby(uid_email_key, 1)
            r.expire(uid_email_key, SecurityConfig.expire_unfinished_timeout * 60)
        raise HTTPException(detail="Invalid Password", status_code=401)
    # Delete Failed attempts on sign in
    r.delete(uid_email_key)
    # Check if 2FA
    if user.get("2fa_secret", None):
        # Validate 2FA
        if not pyotp.TOTP(user["2fa_secret"]).verify(login_form.two_factor_code):
            raise HTTPException(detail="Invalid 2FA Code", status_code=401)
    session_token = create_login_session(user["_id"], request)
    if SessionConfig.auto_cookie:
        response.set_cookie(
            SessionConfig.auto_cookie_name,
            session_token,
            expires=SessionConfig.session_expiry_seconds,
            samesite=SessionConfig.cookie_samesite,
            secure=SessionConfig.cookie_secure,
        )
    return LoginResponse(
        session_token=session_token, expires=SessionConfig.session_expiry_seconds
    )


@router.get("/logout", status_code=204)
async def logout(
    response: Response,
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name),
):
    """
    # Log Out (Delete Session)

    ## Description
    This endpoint is used to log out a user and delete the session.
    """
    response.delete_cookie(
        SessionConfig.auto_cookie_name,
        samesite=SessionConfig.cookie_samesite,
        secure=SessionConfig.cookie_secure,
    )
    delete_session(session_token)
