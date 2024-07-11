from fastapi import APIRouter, Response, BackgroundTasks, HTTPException, Request
from api.model import UserSignupRequest, LoginResponse, ConfirmEmailCodeRequest
from tools import send_email
import json
from tools import SignupConfig, SessionConfig
from tools import all_ids, regenerate_ids, r
from crud.user import create_user, check_unique_usr

router = APIRouter(
    prefix="/signup",
    tags=["Sign Up"],
)

# Create an ExpiringDict object to store temporary accounts (not email verified yet)
"""
temp_accounts["form"]: UserSignupRequest
temp_accounts["code"]: str | int
"""


@router.post(
    "/",
    status_code=200,
    responses={
        409: {"description": "Duplicate Entry"},
        204: {"description": "Confirmation Email Sent"},
        200: {"description": "Account was created successfully."},
    },
    response_model=LoginResponse,
)
async def signup(
    signup_form: UserSignupRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    request: Request,
):
    """
    # Sign Up

    ## Description
    This endpoint is used to sign up a user. Depending on the configuration, a confirmation email is sent to the user.
    """
    # Handle signup
    if SignupConfig.enable_conf_email:
        # Those checks are only needed when confirmation emails are enabled (otherwise, create the user directly and raise duplicate from mongodb)
        # Check if email in confirmation email dict
        if r.get("signup:" + signup_form.email):
            raise HTTPException(detail="E-Mail already sent", status_code=409)
        # Check if user already exists in database
        if check_unique_usr(signup_form.email, signup_form.username):
            raise HTTPException(
                detail="Email or Username already exists", status_code=409
            )
        if not all_ids:
            # Generate new ids
            regenerate_ids()
        # Get a unique ID for confirmation email
        unique_id = all_ids.pop()
        # Save the Account into the expiring dict (delete if user refuses to confirm email in time)
        # Indexed by E-Mail to quickly check if the user has already signed up (O(1))
        r.setex(
            "signup:" + signup_form.email,
            SignupConfig.conf_code_expiry * 60,
            json.dumps({"form": signup_form.model_dump(), "code": unique_id}),
        )

        # Generate and send confirmation email
        background_tasks.add_task(
            send_email,
            "ConfirmEmail",
            signup_form.email,
            code=unique_id,
            time=SignupConfig.conf_code_expiry,
            username=signup_form.username,
        )
        return Response(status_code=204)
    else:
        session_token = create_user(signup_form, background_tasks, request)
        if SessionConfig.auto_cookie:
            response.set_cookie(
                SessionConfig.auto_cookie_name,
                session_token,
                expires=SessionConfig.session_expiry_seconds,
            )
        return LoginResponse(
            session_token=session_token, expires=SessionConfig.session_expiry_seconds
        )


@router.post(
    "/confirm",
    response_model=LoginResponse,
    responses={
        404: {"description": "No Account Found with this code. Or Code expired."},
        200: {"description": "Account was created successfully."},
        409: {"description": "Duplicate Entry"},
    },
)
async def confirm_email(
    payload: ConfirmEmailCodeRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    request: Request,
):
    """
    # Confirm E-Mail

    ## Description
    This endpoint is used to confirm the E-Mail of a user. This is only needed if confirmation E-Mails are enabled.
    """
    acc = r.get("signup:" + payload.email)
    if not acc:
        raise HTTPException(detail="No Account Found with this code.", status_code=404)
    acc = json.loads(acc)
    if str(acc["code"]) != str(payload.code):
        raise HTTPException(detail="Invalid Code", status_code=404)
    # Account is confirmed, create the user
    session_token = create_user(
        None, background_tasks, request, additional_data=acc["form"]
    )
    if SessionConfig.auto_cookie:
        response.set_cookie(
            SessionConfig.auto_cookie_name,
            session_token,
            expires=SessionConfig.session_expiry_seconds,
        )
    r.delete("signup:" + payload.email)
    return LoginResponse(
        session_token=session_token, expires=SessionConfig.session_expiry_seconds
    )
