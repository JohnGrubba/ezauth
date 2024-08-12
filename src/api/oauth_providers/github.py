from fastapi import APIRouter, Request, BackgroundTasks, Response, HTTPException
from fastapi.responses import RedirectResponse
from tools import SignupConfig, SessionConfig
import json
import requests
import random
import re
from crud.user import (
    create_user,
    get_user_by_github_uid,
    get_user_identifier,
    link_github_account,
)
from crud.sessions import create_login_session
from api.model import LoginResponse

try:
    github_cnf = json.load(open("/src/app/config/github_client_secret.env.json"))
except FileNotFoundError:
    raise FileNotFoundError(
        "GitHub OAuth Config File not found (github_client_secret.env.json).\
        Please disable this OAuth Provider, or create the file as described in the Docs."
    )
REDIRECT_URI = SignupConfig.oauth_base_url + "/oauth/github/callback"
CLIENT_ID = github_cnf["client_id"]
CLIENT_SECRET = github_cnf["client_secret"]

router = APIRouter(
    prefix="/github",
    dependencies=[],
)


@router.get("/login")
async def oauth_login():
    """
    # OAuth Login

    ## Description
    This endpoint is used to initiate the OAuth login flow.
    """
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user:email"
    )


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
    if SignupConfig.oauth_redirect_url:
        return RedirectResponse(SignupConfig.oauth_redirect_url)
    return LoginResponse(
        session_token=session_token, expires=SessionConfig.session_expiry_seconds
    )


@router.get("/callback")
async def oauth_callback(
    request: Request, background_tasks: BackgroundTasks, response: Response
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")
    print("Code: ", code)
    rsp = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={"Accept": "application/json"},
    )
    js_resp = rsp.json()
    try:
        access_token = js_resp["access_token"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid code")
    # Request User Information
    rsp = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    ).json()
    # Check if SignIn Possible
    usr = get_user_by_github_uid(rsp["id"])
    if usr:
        return login_usr(response, usr, request)
    # Because you can somehow hide emails on github, we have to query them separately
    email_query = requests.get(
        "https://api.github.com/user/emails",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    primary_email = None
    for email in email_query.json():
        if email["primary"]:
            primary_email = email["email"]
            break
    username = rsp["login"]
    # Validate Username
    if len(username) < 4 or re.search("[^a-zA-Z0-9]", username) is not None:
        username = primary_email.split("@")[0]

    # If users email already exists, link the google account
    usr = get_user_identifier(primary_email)
    if usr:
        link_github_account(usr["_id"], rsp["id"])
        return login_usr(response, usr, request)

    # Check if user already exists in database
    if get_user_identifier(username):
        username += str(random.randint(1000, 9999))

    # Custom SignUp Form (Password Field missing etc.)
    signup_form = {
        "email": primary_email,
        "username": username,
        "password": "",
        "github_uid": rsp["id"],
    }
    # Persist user in DB
    session_token = create_user(signup_form, background_tasks, request, signup_form)
    if SessionConfig.auto_cookie:
        response.set_cookie(
            SessionConfig.auto_cookie_name,
            session_token,
            expires=SessionConfig.session_expiry_seconds,
            samesite=SessionConfig.cookie_samesite,
            secure=SessionConfig.cookie_secure,
        )
    if SignupConfig.oauth_redirect_url:
        return RedirectResponse(SignupConfig.oauth_redirect_url)
    return LoginResponse(
        session_token=session_token, expires=SessionConfig.session_expiry_seconds
    )
