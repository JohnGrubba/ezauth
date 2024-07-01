import uuid
from tools.db import sessions_collection
import datetime
from tools.conf import SessionConfig


def create_login_session(user_id: str) -> str:
    """
    Create a login session for the user.

    Args:
        user_id (str): User ID

    Returns:
        str: Session Token
    """
    # Check maximum amount of sessions
    if (
        sessions_collection.count_documents({"user_id": user_id})
        >= SessionConfig.max_session_count
    ):
        # Delete the oldest session
        sessions_collection.find_one_and_delete(
            {"user_id": user_id}, sort=[("createdAt", 1)]
        )
    session_token = str(uuid.uuid4())
    sessions_collection.insert_one(
        {
            "session_token": session_token,
            "user_id": user_id,
            "createdAt": datetime.datetime.now(),
        }
    )
    return session_token


def check_session(session_token: str) -> bool:
    """
    Check if the session is valid.

    Args:
        session_token (str): Session Token

    Returns:
        bool: True if the session is valid
    """
    return sessions_collection.find_one({"session_token": session_token}) is not None
