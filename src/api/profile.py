from fastapi import APIRouter, Depends, HTTPException, Response, BackgroundTasks
from tools import AccountFeaturesConfig
from api.model import (
    DeleteAccountRequest,
    ProfileUpdateRequest,
    ConfirmEmailCodeRequest,
)
import bcrypt
from crud.user import update_public_user, schedule_delete_user, change_email
from api.dependencies.authenticated import (
    get_pub_user_dep,
    get_dangerous_user_dep,
    get_user_dep,
)
from tools import SessionConfig, r
from crud.user import get_public_user, get_user_identifier
import bson
import json

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("")
async def profile(user: dict = Depends(get_pub_user_dep)):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the public profile information of the user.
    """
    return user


@router.patch("", status_code=200)
async def update_profile(
    update_data: ProfileUpdateRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_user_dep),
):
    """
    # Update Profile Information
    Public user can only update existing fields and viewable fields for him.
    If you want to edit internal columns, use an internal endpoint.

    ## Description
    This endpoint is used to update the profile information of the user.
    """
    return update_public_user(
        user["_id"], update_data.model_dump(exclude_none=True), background_tasks
    )


@router.post("/confirm-email-change", status_code=204)
async def confirm_new_email(
    payload: ConfirmEmailCodeRequest,
    user: dict = Depends(get_user_dep),
):
    """
    # Confirm New Email

    ## Description
    This endpoint is used to confirm the new email of the user.
    """
    acc = r.get("emailchange:" + str(user["_id"]))
    if not acc:
        raise HTTPException(detail="No Account Found with this code.", status_code=404)
    acc = json.loads(acc)
    if str(acc["code"]) != str(payload.code):
        raise HTTPException(detail="Invalid Code", status_code=404)

    # Update Email
    change_email(user["_id"], acc["new-email"])

    r.delete("emailchange:" + str(user["_id"]))


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


@router.get("/{identifier}")
async def get_profile(identifier: str):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the public profile information of a specified user.
    """
    try:
        usr = get_user_identifier(identifier)
        if not usr:
            raise HTTPException(status_code=404, detail="User not found.")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail="User not found.")
    # Hide email
    usr = get_public_user(usr["_id"])
    usr.pop("email")
    return usr
