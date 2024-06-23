from fastapi import APIRouter
from api.model import UserSignupRequest
from tools import db_collection
from tools.mail import send_email
from expiringdict import ExpiringDict

router = APIRouter(
    prefix="/signup",
    tags=["Sign Up"],
    responses={404: {"description": "Not found"}},
    dependencies=[],
)


@router.post("/", status_code=204)
async def signup(signup_form: UserSignupRequest):
    print(signup_form.model_dump())
    db_collection.insert_one(signup_form.model_dump())
    pass


@router.get("/new")
async def new():
    send_email("WelcomeEmail", "nicjontrickshots@gmail.com", username="Jonas")
    pass
