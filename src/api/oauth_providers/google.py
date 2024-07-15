from fastapi import APIRouter, Request, BackgroundTasks, Response, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from tools.conf import SignupConfig
import os, re
from crud.user import (
    create_user,
    get_user_by_google_uid,
    get_user_email_or_username,
    link_google_account,
)
from api.model import LoginResponse
import jwt
from crud.sessions import create_login_session
from tools import SignupConfig, SessionConfig

# Required for HTTP
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter(
    prefix="/google",
    dependencies=[],
)

# Initialize Googles OAuth Flow
flow = Flow.from_client_secrets_file(
    client_secrets_file="/src/app/config/google_client_secret.env.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    redirect_uri=SignupConfig.oauth_base_url + "/oauth/google/callback",
)


@router.get("/login")
async def oauth_login():
    """
    # OAuth Login

    ## Description
    This endpoint is used to initiate the OAuth login flow.
    """
    auth_url, _ = flow.authorization_url()
    return RedirectResponse(auth_url)


def login_usr(response: Response, usr: dict, request: Request) -> LoginResponse:
    # User already exists
    session_token = create_login_session(usr["_id"], request)
    if SessionConfig.auto_cookie:
        response.set_cookie(
            SessionConfig.auto_cookie_name,
            session_token,
            expires=SessionConfig.session_expiry_seconds,
            samesite=SessionConfig.cookie_samesite,
            secure=SessionConfig.cookie_secure,
        )
    return LoginResponse(
        session_token=session_token, expires=SessionConfig.session_expiry_seconds
    )


@router.get("/callback")
async def oauth_callback(
    request: Request, background_tasks: BackgroundTasks, response: Response
):
    """
    # OAuth Callback

    ## Description
    This endpoint is used to handle the OAuth callback.
    """
    # Get Information about user from Google
    try:
        token = flow.fetch_token(authorization_response=request.url.__str__())
    except:
        raise HTTPException(status_code=401, detail="Invalid OAuth Token")
    jwt_id = token["id_token"]
    jwt_decoded = jwt.decode(
        jwt_id, algorithms=["RS256"], options={"verify_signature": False}
    )

    username = jwt_decoded["name"].replace(" ", "")
    # Validate Username
    if len(username) < 4 or re.search("[^a-zA-Z0-9]", username) is not None:
        username = jwt_decoded["email"].split("@")[0]

    # Check if SignIn Possible
    usr = get_user_by_google_uid(jwt_decoded["sub"])
    if usr:
        return login_usr(response, usr, request)

    # If users email already exists, link the google account
    usr = get_user_email_or_username(jwt_decoded["email"])
    if usr:
        link_google_account(usr["_id"], jwt_decoded["sub"])
        return login_usr(response, usr, request)

    # Custom SignUp Form (Password Field missing etc.)
    signup_form = {
        "email": jwt_decoded["email"],
        "username": username,
        "password": "",
        "google_uid": jwt_decoded["sub"],
    }
    # Persist user in DB
    session_token = create_user(None, background_tasks, request, signup_form)
    if SessionConfig.auto_cookie:
        response.set_cookie(
            SessionConfig.auto_cookie_name,
            session_token,
            expires=SessionConfig.session_expiry_seconds,
            samesite=SessionConfig.cookie_samesite,
            secure=SessionConfig.cookie_secure,
        )
    return LoginResponse(
        session_token=session_token, expires=SessionConfig.session_expiry_seconds
    )
