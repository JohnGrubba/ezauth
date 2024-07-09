from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_user_dep
import pyotp
from tools import AccountFeaturesConfig
from crud.user import add_2fa
from expiring_dict import ExpiringDict
from api.model import TwoFactorAddResponse

temp_2fa = ExpiringDict(ttl=30, interval=10)

router = APIRouter(
    prefix="/2fa",
    tags=["TOTP 2FA"],
    dependencies=[Depends(get_user_dep)],
)


@router.post("/enable", response_model=TwoFactorAddResponse)
async def enable_2fa(
    user=Depends(get_user_dep),
):
    """
    # Enable 2FA

    ## Description
    This endpoint is used to enable 2FA for the user.
    """
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
    return TwoFactorAddResponse(provision_uri=prov_url)


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
