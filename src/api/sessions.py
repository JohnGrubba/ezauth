from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from api.dependencies.authenticated import get_user_dep
from tools import bson_to_json, SessionConfig
from crud.sessions import get_user_sessions, delete_session, get_session_by_id
from api.model import SessionListResponseModel
from bson import ObjectId

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    dependencies=[Depends(get_user_dep)],
)


@router.get("", response_model=SessionListResponseModel)
async def sessions_list(
    user: dict = Depends(get_user_dep),
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name),
):
    """
    # Get Sessions

    ## Description
    This endpoint is used to get the sessions of the user.
    """
    sesss = get_user_sessions(user["_id"])

    def mark_own_session(session: dict):
        session = bson_to_json(session)
        if session["session_token"] == session_token:
            session["is_current"] = True
        return session

    return {"sessions": [mark_own_session(sess) for sess in sesss]}


@router.delete("/{session_id}")
async def delete_other_session(session_id: str, user: dict = Depends(get_user_dep)):
    """
    # Delete Session

    ## Description
    This endpoint is used to delete a session.
    """
    sess_to_delete = get_session_by_id(session_id)
    if not sess_to_delete:
        raise HTTPException(status_code=404, detail="Session not found.")
    if ObjectId(sess_to_delete["user_id"]) != ObjectId(user["_id"]):
        raise HTTPException(status_code=404, detail="Session not found.")
    delete_session(sess_to_delete["session_token"])
    return Response(status_code=204)
