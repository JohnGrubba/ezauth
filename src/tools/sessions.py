import uuid
from tools.db import sessions_collection
import datetime


def create_login_session(user_id: str) -> str:
    """
    Create a login session for the user.
    """
    session_token = str(uuid.uuid4())
    sessions_collection.insert_one(
        {
            "session_token": session_token,
            "user_id": user_id,
            "createdAt": datetime.datetime.now(),
        }
    )
    return session_token
