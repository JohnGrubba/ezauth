from fastapi import APIRouter, HTTPException, Response, Cookie, Request
from api.model import LoginRequest, LoginResponse
from crud.user import get_user_email_or_username
from crud.sessions import create_login_session, delete_session
import bcrypt
import pyotp
from tools import SessionConfig, r, SecurityConfig

router = APIRouter(
    prefix="",
    tags=["Log In"],
)


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
    user = get_user_email_or_username(login_form.identifier)
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
