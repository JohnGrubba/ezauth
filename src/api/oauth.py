from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter(
    prefix="/oauth",
    tags=["OAuth"],
    dependencies=[],
)

flow = Flow.from_client_secrets_file(
    client_secrets_file="/src/app/config/client_secret.env.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    redirect_uri="http://localhost:3250/oauth/callback",
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


@router.get("/callback")
async def oauth_callback(request: Request):
    """
    # OAuth Callback

    ## Description
    This endpoint is used to handle the OAuth callback.
    """
    print()
    token = flow.fetch_token(authorization_response=request.url.__str__())
    print(token)
    return {"status": "ok"}
