from fastapi import APIRouter, HTTPException, Response
from api.model import LoginRequest, LoginResponse
from crud.user import get_user_email_or_username
from crud.sessions import create_login_session
import bcrypt
from tools.conf import SessionConfig

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
    },
    response_model=LoginResponse,
)
async def login(login_form: LoginRequest, response: Response):
    """
    # Log In (Create Session)

    ## Description
    This endpoint is used to log in a user and create a session.
    Returns a session token if the credentials are correct.
    Can also return a `Set-Cookie` header with the session token. (See Config)
    """
    user = get_user_email_or_username(login_form.identifier)
    if user is None:
        raise HTTPException(status_code=404)
    # Check Password
    if bcrypt.checkpw(
        login_form.password.get_secret_value().encode("utf-8"),
        user["password"].encode("utf-8"),
    ):
        session_token = create_login_session(user["_id"])
        if SessionConfig.auto_cookie:
            response.set_cookie(
                SessionConfig.auto_cookie_name,
                session_token,
                expires=SessionConfig.session_expiry_seconds,
            )
        return LoginResponse(session_token=session_token)
    raise HTTPException(detail="Invalid Password", status_code=401)
