from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    BackgroundTasks,
    UploadFile,
)
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
from tools import SessionConfig, r, bson_to_json
from crud.user import get_public_user, get_user_identifier
import bson
import json
import io
from PIL import Image, ImageSequence

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
    return bson_to_json(
        update_public_user(
            user["_id"], update_data.model_dump(exclude_none=True), background_tasks
        )
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
    You can use either email, username or user_id for this endpoint.
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
    return bson_to_json(usr)


@router.post("/picture", status_code=200)
async def upload_profile_picture(
    pic: UploadFile,
    user: dict = Depends(get_user_dep),
):
    """
    # Upload Profile Picture

    ## Description
    This endpoint is used to upload a profile picture for the user.

    Uploaded Images are resized and optimized to WebP format.
    Images can be accessed via `/cdn/<user_id>.webp`.
    If the user has no profile picture, the default profile picture will be used. (default.webp in /uploads)
    """
    if not AccountFeaturesConfig.allow_profile_picture:
        raise HTTPException(
            status_code=403, detail="Profile Picture is disabled for this instance."
        )
    # Check if the uploaded file is an image
    if not pic.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only images / gifs are allowed."
        )

    # Check file size (limit to 10 MB)
    if pic.size > AccountFeaturesConfig.max_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the {AccountFeaturesConfig.max_size_mb} MB limit.",
        )

    try:
        image = Image.open(io.BytesIO(await pic.read()))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Image File.")

    if image.format == "GIF" and not AccountFeaturesConfig.allow_gif:
        raise HTTPException(
            status_code=400, detail="GIFs are not allowed for profile pictures."
        )

    # Handle GIFs
    if image.format == "GIF" and AccountFeaturesConfig.allow_gif:
        frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
        if len(frames) > AccountFeaturesConfig.max_gif_frames:
            raise HTTPException(
                status_code=400,
                detail="GIFs with more than 200 frames are not allowed.",
            )
        resized_frames = []
        for frame in frames:
            frame = frame.convert("RGBA")
            frame = resize_and_crop_image(frame)
            resized_frames.append(frame)
        image = resized_frames[0]
        image.save(
            f"/uploads/{user['_id']}.webp",
            save_all=True,
            append_images=resized_frames[1:],
            format="webp",
            optimize=True,
            quality=AccountFeaturesConfig.profile_picture_quality,
        )
    else:
        image = resize_and_crop_image(image)
        save_path = f"/uploads/{user['_id']}.webp"
        image.save(
            save_path,
            "webp",
            optimize=True,
            quality=AccountFeaturesConfig.profile_picture_quality,
        )


def resize_and_crop_image(image):
    # Crop the image to a square from the center
    width, height = image.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    image = image.crop((left, top, right, bottom))

    # Resize the image to 128x128
    image = image.resize(
        (
            AccountFeaturesConfig.profile_picture_resize_width,
            AccountFeaturesConfig.profile_picture_resize_height,
        ),
        Image.Resampling.NEAREST,
    )
    return image
