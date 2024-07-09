from fastapi import APIRouter, Header, HTTPException, Depends, BackgroundTasks
from tools import broadcast_emails, InternalConfig, bson_to_json
from api.model import BroadCastEmailRequest, InternalProfileRequest
from crud.user import get_user, get_batch_users
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
async def profile(internal_req: InternalProfileRequest):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the whole profile information of the user. (Including Internal Information)
    """
    sess = (
        get_session(internal_req.session_token) if internal_req.session_token else None
    )
    return bson_to_json(get_user(sess["user_id"] if sess else internal_req.user_id))


@router.get("/batch-users")
async def batch_users(user_ids_req: str):
    """
    # Get Batch User Information

    ## Description
    This endpoint is used to get the whole profile information of multiple users. (Including Internal Information)

    ## Query Parameters
    - **user_ids**: List of User IDs seperated by `,`
    """
    ids = user_ids_req.split(",")
    if len(ids) > 50:
        raise HTTPException(
            status_code=400, detail="Too many User IDs. Max 50 User IDs allowed."
        )
    return [bson_to_json(_) for _ in get_batch_users(ids)]
