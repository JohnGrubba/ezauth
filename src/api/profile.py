from fastapi import APIRouter, Depends, HTTPException, Response
from tools import AccountFeaturesConfig
from api.model import DeleteAccountRequest
import bcrypt
from crud.user import update_public_user, schedule_delete_user
from api.dependencies.authenticated import (
    get_pub_user_dep,
    get_dangerous_user_dep,
    get_user_dep,
)
from tools import SessionConfig

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
    if user["password"]:
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
