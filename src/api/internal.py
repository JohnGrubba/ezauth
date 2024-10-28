from fastapi import APIRouter, Header, HTTPException, Depends, BackgroundTasks
from tools import broadcast_emails, InternalConfig, bson_to_json, r
from api.model import (
    BroadCastEmailRequest,
    InternalProfileRequest,
    InternalUserQuery,
    InternalUserCreateRequest,
)
from typing import List
from crud.user import (
    get_user,
    get_batch_users,
    update_public_user,
    query_users,
    remove_user,
    restore_usr,
    count_users,
    count_oauth,
    bulk_crt_users,
)
from crud.sessions import get_session, count_sessions
from threading import Lock
from api.helpers.extension_loader import modules

email_task_running = Lock()


async def check_internal_key(
    internal_api_key: str = Header(default=None, alias="internal-api-key")
):
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


@router.post("/broadcast-email", status_code=204)
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


@router.patch("/profile")
async def update_profile(
    internal_req: InternalProfileRequest,
    background_tasks: BackgroundTasks,
    update_data: dict,
):
    """
    # Update Profile Information

    ## Description
    This endpoint is used to update the profile information of the user.
    """
    sess = (
        get_session(internal_req.session_token) if internal_req.session_token else None
    )
    usr = get_user(sess["user_id"] if sess else internal_req.user_id)
    return bson_to_json(
        update_public_user(usr["_id"], update_data, background_tasks, True)
    )


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


@router.post("/users")
async def query_users_paginated(query: InternalUserQuery):
    """
    # Query Users

    ## Description
    This endpoint is used to query users based on the query string provided.

    ## Query Parameters
    - **query**: Query String
    """
    return [bson_to_json(_) for _ in query_users(query.query, query.sort, query.page)]


@router.delete("/removeuser", status_code=204)
async def remove_user_instant(user_id: str):
    """
    # Remove User

    ## Description
    This endpoint is used to remove a user from the database instantly.
    """
    remove_user(user_id)


@router.put("/restoreuser", status_code=204)
async def restore_user(user_id: str):
    """
    # Restore User

    ## Description
    This endpoint is used to restore a user from the database.
    """
    restore_usr(user_id)


@router.get("/stats")
async def stats():
    """
    # Get Stats (Ressource Intensive)

    ## Description
    This endpoint is used to get stats about the application.
    """
    usr_count = count_users()
    sess_count = count_sessions()
    return {
        "users": usr_count,
        "sessions": sess_count,
        "avg_sess_per_usr": sess_count / usr_count if usr_count else 0,
        **count_oauth(),
        "pending_users": len(r.scan(match="signup:*")[1]),
        "loaded_extensions": [
            {"name": module.__name__, "readme": readme, "status": loaded}
            for spec, module, readme, loaded in modules
        ],
    }


@router.post("/create-user", status_code=204)
async def bulk_create_users(req: List[InternalUserCreateRequest]):
    """
    # Create User

    ## Description
    This endpoint is used to bulk create users.
    The users have no password when created, and have to click forgot password to set one.
    So a correct E-Mail for the Users is mandatory.
    """
    bulk_crt_users(req)
