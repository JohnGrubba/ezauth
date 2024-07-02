from fastapi import HTTPException, Cookie
from tools import SessionConfig, InternalConfig
from tools import users_collection, sessions_collection
import logging


async def get_pub_user(
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name)
):
    if not session_token:
        logging.debug("No session token")
        raise HTTPException(status_code=401)
    session = sessions_collection.find_one({"session_token": session_token})
    if not session:
        logging.debug("No session found")
        raise HTTPException(status_code=401)
    user = users_collection.find_one(
        {"_id": session["user_id"]}, InternalConfig.internal_columns
    )
    if not user:
        logging.debug("No user for session found")
        raise HTTPException(status_code=401)
    return user
