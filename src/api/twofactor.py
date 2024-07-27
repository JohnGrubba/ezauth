from fastapi import APIRouter, Depends, HTTPException, Response
from api.dependencies import get_dangerous_user_dep
import pyotp
import bson
from tools import AccountFeaturesConfig, r
from crud.user import add_2fa
from api.model import TwoFactorAddResponse, ConfirmationCode
from qrcode.main import QRCode
import qrcode.image.svg

router = APIRouter(
    prefix="/2fa",
    tags=["TOTP 2FA"],
    dependencies=[Depends(get_dangerous_user_dep)],
)


def enable_2fa_temp(user: dict) -> str:
    # Check if user already has 2FA
    if user.get("2fa_secret", None):
        raise HTTPException(status_code=400, detail="2FA already enabled.")
    if not AccountFeaturesConfig.enable_2fa:
        raise HTTPException(status_code=403, detail="2FA is disabled.")
    # Generate a new secret
    secret_bytes = pyotp.random_base32()
    totp = pyotp.TOTP(secret_bytes)

    # Generate provisioning URL
    prov_url = totp.provisioning_uri(
        name=user["email"],
        issuer_name=AccountFeaturesConfig.issuer_name_2fa,
        image=AccountFeaturesConfig.issuer_image_url_2fa,
    )
    # Set the secret in Redis (for confirmation)
    r.setex("2fa:" + bson.ObjectId(user["_id"]).__str__(), 60, secret_bytes)
    # Return the provisioning URL for further processing
    return prov_url


@router.post("/enable", response_model=TwoFactorAddResponse)
async def enable_2fa(
    user=Depends(get_dangerous_user_dep),
):
    """
    # Enable 2FA

    ## Description
    This endpoint is used to enable 2FA for the user.
    """
    return TwoFactorAddResponse(provision_uri=enable_2fa_temp(user))


@router.get(
    "/enable",
    responses={200: {"content": {"image/svg+xml": {}}}},
    response_class=Response,
)
async def enable_2fa_qr(user=Depends(get_dangerous_user_dep)):
    """
    # Enable 2FA QR

    ## Description
    This endpoint is used to get the QR code to enable 2FA for the user.
    """
    if not AccountFeaturesConfig.qr_code_endpoint_2fa:
        raise HTTPException(status_code=403, detail="QR Code endpoint is disabled.")
    prov_url = enable_2fa_temp(user)
    # Generate QR Code for the Provisioning URL
    qr = QRCode(image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(prov_url)
    return Response(qr.make_image().to_string(), media_type="image/svg+xml")


@router.post(
    "/confirm-enable",
    responses={
        400: {"description": "2FA activation expired"},
        204: {"description": "2FA enabled"},
    },
    status_code=204,
)
async def confirm_enable_2fa(
    code: ConfirmationCode, user=Depends(get_dangerous_user_dep)
):
    """
    # Confirm Enable 2FA

    ## Description
    This endpoint is used to confirm the enablement of 2FA for the user.
    """
    # Retrieve Secret from redis
    secret = r.get("2fa:" + bson.ObjectId(user["_id"]).__str__())
    if not secret:
        raise HTTPException(status_code=400, detail="2FA activation expired")
    # Initialize TOTP Generator from the Secret
    totp = pyotp.TOTP(secret)
    if totp.verify(str(code.code)):
        # Persist 2FA in the Database
        add_2fa(user["_id"], secret)
        r.delete("2fa:" + bson.ObjectId(user["_id"]).__str__())
    else:
        raise HTTPException(status_code=400, detail="Invalid code")
