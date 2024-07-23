import uuid
from tools.db import sessions_collection
import datetime
from tools.conf import SessionConfig
from fastapi import Request
from user_agents import parse
from bson import ObjectId


def create_login_session(user_id: ObjectId, request: Request) -> str:
    """
    Create a login session for the user.

    Args:
        user_id (str): User ID
        request (Request): Request Object (For Device Information Extraction)

    Returns:
        str: Session Token
    """
    u_agent = request.headers.get("User-Agent")
    ua = parse(u_agent)
    device_information = {
        "is_mobile": ua.is_mobile,
        "is_tablet": ua.is_tablet,
        "is_pc": ua.is_pc,
        "is_touch_capable": ua.is_touch_capable,
        "is_bot": ua.is_bot,
        "device_name": ua.get_device(),
        "browser_name": ua.get_browser(),
        "os_name": ua.get_os(),
    }
    # Check maximum amount of sessions
    if (
        sessions_collection.count_documents({"user_id": user_id})
        >= SessionConfig.max_session_count
    ):
        # Delete the oldest session
        sessions_collection.find_one_and_delete(
            {"user_id": user_id}, sort=[("createdAt", 1)]
        )
    # Generate a new session token
    session_token = str(uuid.uuid4())
    # Persist the session
    sessions_collection.insert_one(
        {
            "session_token": session_token,
            "user_id": user_id,
            "createdAt": datetime.datetime.now(),
            "device_information": device_information,
        }
    )
    return session_token


def get_session(session_token: str) -> dict:
    """
    Check if the session is valid and return the session information.

    Args:
        session_token (str): Session Token

    Returns:
        dict: Session Information
    """
    return sessions_collection.find_one({"session_token": session_token})


def delete_session(session_token: str) -> bool:
    """
    Delete a session.

    Args:
        session_token (str): Session Token

    Returns:
        bool: True if the session was deleted
    """
    return (
        sessions_collection.find_one_and_delete({"session_token": session_token})
        is not None
    )


def get_user_sessions(user_id: str) -> list:
    """
    Get all sessions for a user.

    Args:
        user_id (str): User ID

    Returns:
        list: List of Sessions
    """
    return list(sessions_collection.find({"user_id": user_id}))


def get_session_by_id(session_id: str) -> dict:
    """
    Get a session by ID.

    Args:
        session_id (str): Session ID

    Returns:
        dict: Session Information
    """
    return sessions_collection.find_one({"_id": ObjectId(session_id)})
