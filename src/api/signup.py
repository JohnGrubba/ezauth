from fastapi import APIRouter
from api.model import UserSignupRequest
from tools import db_collection
from tools.mail import send_email
from tools import SignupConfig
from expiring_dict import ExpiringDict

temp_accounts = ExpiringDict(ttl=SignupConfig.conf_code_expiry, interval=10)

router = APIRouter(
    prefix="/signup",
    tags=["Sign Up"],
    responses={404: {"description": "Not found"}},
    dependencies=[],
)


@router.post("/", status_code=204)
async def signup(signup_form: UserSignupRequest):
    pass
