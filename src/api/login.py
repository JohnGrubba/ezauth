from fastapi import APIRouter, Response
from api.model import LoginRequest
from crud.user import get_user_email_or_username
from crud.sessions import create_login_session
import bcrypt

router = APIRouter(
    prefix="/login",
    tags=["Log In"],
)


@router.post(
    "/",
    status_code=200,
    responses={
        401: {"description": "Invalid Credentials"},
        404: {"description": "User not found"},
        200: {"description": "Login Successful"},
    },
)
async def login(login_form: LoginRequest):
    user = get_user_email_or_username(login_form.identifier)
    if user is None:
        return Response(status_code=404)
    # Check Password
    if bcrypt.checkpw(
        login_form.password.get_secret_value().encode("utf-8"),
        user["password"].encode("utf-8"),
    ):
        return create_login_session(user["_id"])
    return Response(status_code=401)
