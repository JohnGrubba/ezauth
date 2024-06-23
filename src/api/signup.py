from fastapi import APIRouter
from api.model import UserSignupRequest
from tools import db_collection

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
