from fastapi import APIRouter, Depends, Cookie, HTTPException, BackgroundTasks
from tools.conf import SessionConfig, AccountFeaturesConfig, SignupConfig
from api.model import PasswordHashed
from crud.user import change_pswd
from api.dependencies.authenticated import get_pub_user
from crud.user import get_user
from crud.sessions import get_session
from tools import send_email, all_ids, regenerate_ids
from expiring_dict import ExpiringDict

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    dependencies=[Depends(get_pub_user)],
)

temp_changes = ExpiringDict(ttl=SignupConfig.conf_code_expiry * 60, interval=10)


@router.get("/")
async def profile(user: dict = Depends(get_pub_user)):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the public profile information of the user.
    """
    return user


@router.post("/change-password", status_code=204)
async def change_password(
    new_password: PasswordHashed,
    background_tasks: BackgroundTasks,
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name),
    public_user: dict = Depends(get_pub_user),
):
    """
    # Change Password

    ## Description
    This endpoint is used to change the password of the user.
    """
    if not AccountFeaturesConfig.enable_change_password:
        raise HTTPException(status_code=403, detail="Changing Password is disabled.")
    sess = get_session(session_token)
    if not sess:
        raise HTTPException(status_code=401)
    user = get_user(sess["user_id"])
    # Send Confirmation E-Mail (If enabled)
    if AccountFeaturesConfig.change_password_confirm_email:
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
async def confirm_password(
    code: str | int,
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name),
):
    """
    # Confirm Password Change

    ## Description
    This endpoint is used to confirm a password change.
    """
    sess = get_session(session_token)
    if not sess:
        raise HTTPException(status_code=401)
    user = get_user(sess["user_id"])
    if not AccountFeaturesConfig.enable_change_password:
        raise HTTPException(status_code=403, detail="Changing Password is disabled.")
    try:
        change_req = temp_changes[user["email"]]
    except KeyError:
        raise HTTPException(status_code=404, detail="No Password Change Request found.")
    # Check code
    if change_req["code"] != code:
        raise HTTPException(status_code=401, detail="Invalid Code")

    change_pswd(user["_id"], change_req["new_pswd"])
    del temp_changes[user["email"]]
