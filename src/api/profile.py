from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from tools.conf import AccountFeaturesConfig, SignupConfig
from api.model import ResetPasswordRequest, ConfirmEmailRequest, DeleteAccountRequest
import json
import bcrypt
from crud.user import change_pswd, update_public_user, schedule_delete_user
from api.dependencies.authenticated import (
    get_pub_user_dep,
    get_dangerous_user_dep,
    get_user_dep,
)
from tools import send_email, all_ids, regenerate_ids, r, SessionConfig

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    dependencies=[Depends(get_pub_user_dep)],
)


@router.get("")
async def profile(user: dict = Depends(get_pub_user_dep)):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the public profile information of the user.
    """
    return user


@router.post(
    "/reset-password",
    status_code=204,
    responses={
        204: {"description": "Password Reset Email Sent"},
        403: {"description": "Resetting Password is disabled."},
        409: {
            "description": "Password Reset Email already sent. You have one request pending."
        },
        401: {"description": "Invalid Old Password"},
        200: {"description": "Password Reset Successfully"},
    },
)
async def reset_password(
    password_reset_form: ResetPasswordRequest,
    background_tasks: BackgroundTasks,
    user=Depends(get_dangerous_user_dep),
    public_user: dict = Depends(get_pub_user_dep),
):
    """
    # Reset Password

    ## Description
    This endpoint is used to reset the password of the user.
    """
    if not AccountFeaturesConfig.enable_reset_pswd:
        raise HTTPException(status_code=403, detail="Resetting Password is disabled.")

    # If user has old password, validate it, else don't care about that field
    # He only has OAuth signin so far, so let him reset
    if user.get("password", None):
        # Check Password
        if not bcrypt.checkpw(
            password_reset_form.old_password.get_secret_value().encode("utf-8"),
            user["password"].encode("utf-8"),
        ):
            raise HTTPException(detail="Invalid Old Password", status_code=401)

    # Send Confirmation E-Mail (If enabled)
    if AccountFeaturesConfig.reset_pswd_conf_mail:
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
    else:
        change_pswd(user["_id"], password_reset_form.password)
        return Response(status_code=200)


@router.post("/confirm-password", status_code=204, responses={
    204: {"description": "Password Reset Successfully"},
    403: {"description": "Resetting Password is disabled."},
    404: {"description": "No Password Reset Request found."},
    401: {"description": "Invalid Code"},
})
async def confirm_password(code: ConfirmEmailRequest, user=Depends(get_user_dep)):
    """
    # Confirm Password Reset

    ## Description
    This endpoint is used to confirm a password reset.
    """
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


@router.patch("", status_code=200)
async def update_profile(update_data: dict, user: dict = Depends(get_user_dep)):
    """
    # Update Profile Information
    Public user can only update existing fields and viewable fields for him.
    If you want to edit internal columns, use an internal endpoint.

    ## Description
    This endpoint is used to update the profile information of the user.
    """
    return update_public_user(user["_id"], update_data)


@router.delete("", status_code=204)
async def delete_account(
    password: DeleteAccountRequest,
    response: Response,
    user: dict = Depends(get_dangerous_user_dep),
):
    """
    # Delete Account

    ## Description
    This endpoint is used to request a deletion of the user's account.
    This process can only be canceled by the administration of the system.
    """
    if not AccountFeaturesConfig.allow_deletion:
        raise HTTPException(status_code=403, detail="Account Deletion is disabled.")
    # Check Password
    if not bcrypt.checkpw(
        password.password.get_secret_value().encode("utf-8"),
        user["password"].encode("utf-8"),
    ):
        raise HTTPException(detail="Invalid Password", status_code=401)
    schedule_delete_user(user["_id"])
    response.delete_cookie(
        SessionConfig.auto_cookie_name,
        samesite=SessionConfig.cookie_samesite,
        secure=SessionConfig.cookie_secure,
    )
