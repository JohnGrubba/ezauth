from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from tools.conf import AccountFeaturesConfig, SignupConfig
from api.model import PasswordHashed
from crud.user import change_pswd, update_public_user
from api.dependencies.authenticated import get_pub_user_dep, get_user_dep
from tools import send_email, all_ids, regenerate_ids
from expiring_dict import ExpiringDict

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    dependencies=[Depends(get_pub_user_dep)],
)

temp_changes = ExpiringDict(ttl=SignupConfig.conf_code_expiry * 60, interval=10)


@router.get("/")
async def profile(user: dict = Depends(get_pub_user_dep)):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the public profile information of the user.
    """
    return user


@router.post("/reset-password", status_code=204)
async def reset_password(
    new_password: PasswordHashed,
    background_tasks: BackgroundTasks,
    user=Depends(get_user_dep),
    public_user: dict = Depends(get_pub_user_dep),
):
    """
    # Reset Password

    ## Description
    This endpoint is used to reset the password of the user.
    """
    if not AccountFeaturesConfig.enable_reset_password:
        raise HTTPException(status_code=403, detail="Resetting Password is disabled.")
    # Send Confirmation E-Mail (If enabled)
    if AccountFeaturesConfig.reset_password_confirm_email:
        if not all_ids:
            # Generate new ids
            regenerate_ids()
        # Get a unique ID for confirmation email
        unique_id = all_ids.pop()
        temp_changes[user["email"]] = {
            "action": "password_reset",
            "code": unique_id,
            "new_pswd": new_password.password,
        }
        background_tasks.add_task(
            send_email,
            "ChangePassword",
            user["email"],
            code=unique_id,
            time=SignupConfig.conf_code_expiry,
            **public_user,
        )
    else:
        change_pswd(user["_id"], new_password.password)


@router.post("/confirm-password", status_code=204)
async def confirm_password(code: str | int, user=Depends(get_user_dep)):
    """
    # Confirm Password Reset

    ## Description
    This endpoint is used to confirm a password reset.
    """
    if not AccountFeaturesConfig.enable_reset_password:
        raise HTTPException(status_code=403, detail="Resetting Password is disabled.")
    try:
        change_req = temp_changes[user["email"]]
    except KeyError:
        raise HTTPException(status_code=404, detail="No Password Reset Request found.")
    # Check code
    if change_req["code"] != code:
        raise HTTPException(status_code=401, detail="Invalid Code")

    change_pswd(user["_id"], change_req["new_pswd"])
    del temp_changes[user["email"]]


@router.patch("/", status_code=200)
async def update_profile(update_data: dict, user: dict = Depends(get_user_dep)):
    """
    # Update Profile Information
    Public user can only update existing fields and viewable fields for him.
    If you want to edit internal columns, use an internal endpoint.

    ## Description
    This endpoint is used to update the profile information of the user.
    """
    return update_public_user(user["_id"], update_data)
