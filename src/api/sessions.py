from fastapi import APIRouter, Depends, Response, HTTPException
from api.dependencies.authenticated import get_user_dep
from tools import bson_to_json
from crud.sessions import get_user_sessions, delete_session, get_session_by_id
from api.model import SessionListResponseModel
from bson import ObjectId

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    dependencies=[Depends(get_user_dep)],
)


@router.get("", response_model=SessionListResponseModel)
async def sessions_list(user: dict = Depends(get_user_dep)):
    """
    # Get Sessions

    ## Description
    This endpoint is used to get the sessions of the user.
    """
    sesss = get_user_sessions(user["_id"])
    sesss = [bson_to_json(sess) for sess in sesss]
    return {"sessions": sesss}


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
