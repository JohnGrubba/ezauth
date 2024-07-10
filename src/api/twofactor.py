from fastapi import APIRouter, Depends, HTTPException, Response
from api.dependencies import get_user_dep
import pyotp
from tools import AccountFeaturesConfig
from crud.user import add_2fa
from expiring_dict import ExpiringDict
from api.model import TwoFactorAddResponse
from qrcode.main import QRCode
import qrcode.image.svg
from tools.conf import AccountFeaturesConfig

temp_2fa = ExpiringDict(ttl=30, interval=10)

router = APIRouter(
    prefix="/2fa",
    tags=["TOTP 2FA"],
    dependencies=[Depends(get_user_dep)],
)


def enable_2fa_temp(user: dict) -> str:
    if not AccountFeaturesConfig.enable_2fa:
        raise HTTPException(status_code=403, detail="2FA is disabled.")
    # Generate a new secret
    secret_bytes = pyotp.random_base32()
    totp = pyotp.TOTP(secret_bytes)

    prov_url = totp.provisioning_uri(
        name=user["email"],
        issuer_name=AccountFeaturesConfig.issuer_name_2fa,
        image=AccountFeaturesConfig.issuer_image_url_2fa,
    )
    temp_2fa[user["_id"]] = secret_bytes
    return prov_url


@router.post("/enable", response_model=TwoFactorAddResponse)
async def enable_2fa(
    user=Depends(get_user_dep),
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
async def enable_2fa_qr(user=Depends(get_user_dep)):
    """
    # Enable 2FA QR

    ## Description
    This endpoint is used to get the QR code to enable 2FA for the user.
    """
    if not AccountFeaturesConfig.qr_code_endpoint_2fa:
        raise HTTPException(status_code=403, detail="QR Code endpoint is disabled.")
    prov_url = enable_2fa_temp(user)
    qr = QRCode(image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(prov_url)
    return Response(qr.make_image().to_string(), media_type="image/svg+xml")


@router.post("/confirm-enable")
async def confirm_enable_2fa(code: str, user=Depends(get_user_dep)):
    """
    # Confirm Enable 2FA

    ## Description
    This endpoint is used to confirm the enablement of 2FA for the user.
    """
    try:
        secret = temp_2fa[user["_id"]]
    except KeyError:
        raise HTTPException(status_code=400, detail="2FA activation expired")
    totp = pyotp.TOTP(secret)
    if totp.verify(code):
        # Persist 2FA in the Database
        add_2fa(user["_id"], secret)
        del temp_2fa[user["_id"]]
