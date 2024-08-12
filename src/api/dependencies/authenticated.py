from fastapi import HTTPException, Cookie
from tools import SessionConfig
from crud.user import get_public_user, get_user, get_dangerous_user
from crud.sessions import extend_session, get_session
import logging


def session_token_used(session: str):
    extend_session(session)


async def get_pub_user_dep(
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name)
):
    """Gets Public User Data from the session token (Dependency)

    Args:
        session_token (str, optional): Session Token. Defaults to Cookie(default=None, alias=SessionConfig.auto_cookie_name).

    Raises:
        HTTPException: No Session Token
        HTTPException: No Session Found
        HTTPException: No User for Session Found

    Returns:
        User: User Dictionary
    """
    if not session_token:
        logging.debug("No session token")
        raise HTTPException(status_code=401)
    session = get_session(session_token)
    if not session:
        logging.debug("No session found")
        raise HTTPException(status_code=401)
    user = get_public_user(session["user_id"])
    if not user:
        logging.debug("No user for session found")
        raise HTTPException(status_code=401)
    session_token_used(session)
    return user


async def get_user_dep(
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name)
):
    """Gets Private User Data from the session token (Dependency)

    Args:
        session_token (str, optional): Session Token. Defaults to Cookie(default=None, alias=SessionConfig.auto_cookie_name).

    Raises:
        HTTPException: No Session Token
        HTTPException: No Session Found
        HTTPException: No User for Session Found

    Returns:
        User: User Dictionary
    """
    if not session_token:
        logging.debug("No session token")
        raise HTTPException(status_code=401)
    session = get_session(session_token)
    if not session:
        logging.debug("No session found")
        raise HTTPException(status_code=401)
    user = get_user(session["user_id"])
    if not user:
        logging.debug("No user for session found")
        raise HTTPException(status_code=401)
    session_token_used(session)
    return user


async def get_dangerous_user_dep(
    session_token: str = Cookie(default=None, alias=SessionConfig.auto_cookie_name)
):
    """!! DANGEROUS !! This includes all Auth Credentials. Gets Internal User Data from the session token (Dependency).

    Args:
        session_token (str, optional): Session Token. Defaults to Cookie(default=None, alias=SessionConfig.auto_cookie_name).

    Raises:
        HTTPException: No Session Token
        HTTPException: No Session Found
        HTTPException: No User for Session Found

    Returns:
        User: User Dictionary
    """
    if not session_token:
        logging.debug("No session token")
        raise HTTPException(status_code=401)
    session = get_session(session_token)
    if not session:
        logging.debug("No session found")
        raise HTTPException(status_code=401)
    user = get_dangerous_user(session["user_id"])
    if not user:
        logging.debug("No user for session found")
        raise HTTPException(status_code=401)
    session_token_used(session)
    return user
