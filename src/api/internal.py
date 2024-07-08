from fastapi import APIRouter, Header, HTTPException, Depends, BackgroundTasks
from tools import broadcast_emails, InternalConfig, bson_to_json
from api.model import BroadCastEmailRequest
from crud.user import get_user
from crud.sessions import get_session
from threading import Lock


email_task_running = Lock()


async def check_internal_key(internal_api_key: str = Header(default=None)):
    if not internal_api_key:
        raise HTTPException(status_code=401)
    if internal_api_key != InternalConfig.internal_api_key:
        raise HTTPException(status_code=401)


router = APIRouter(
    prefix="/internal",
    tags=["Internal API"],
    dependencies=[Depends(check_internal_key)],
)


@router.get("/health")
async def health():
    """
    # Check Health / API Key

    ## Description
    This endpoint is used to check the health of the API and the API Key.
    Can also be used to check if `/internal` endpoints are blocked from public access.
    """
    return {"status": "ok"}


@router.post("/broadcast-email", responses={200: {"description": "E-Mails Queued"}})
async def broadcast_email(
    broadcast_request: BroadCastEmailRequest, background_tasks: BackgroundTasks
):
    """
    # Broadcast a E-Mail Template to all Users

    ## Description
    This endpoint is used to broadcast a E-Mail Template to all users.
    """
    if not email_task_running.acquire_lock(False):
        raise HTTPException(status_code=409, detail="E-Mail Task already running")
    background_tasks.add_task(
        broadcast_emails,
        broadcast_request.template_name,
        email_task_running,
        broadcast_request.mongodb_search_condition,
    )
    return {"status": "E-Mail Task Started"}


@router.post("/profile")
async def profile(session_token: str = Header(default=None)):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the whole profile information of the user. (Including Internal Information)
    """
    sess = get_session(session_token)
    return bson_to_json(get_user(sess["user_id"]))
