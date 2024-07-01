from crud import sessions
from tools import users_collection, SignupConfig, send_email
from fastapi import Response
from api.model import UserSignupRequest, LoginResponse
import pymongo


def check_unique_usr(email: str, username: str) -> bool:
    """Check if the email or username is already in use

    Args:
        email (str): Email
        username (str): Username

    Returns:
        bool: True if email or username is already in use
    """
    return users_collection.find_one(
        {"$or": [{"email": email}, {"username": username}]}
    )


def create_user(signup_model: UserSignupRequest) -> Response:
    """Creates a User in the Database

    Args:
        signup_model (UserSignupRequest): User Data

    Returns:
        Response: Request Response
    """
    # Save the Account into the database
    try:
        user_db = users_collection.insert_one(signup_model.model_dump())
    except pymongo.errors.DuplicateKeyError:
        return Response("Email or Username already exists.", status_code=409)
    # User Created (Create Session Token and send Welcome Email)
    session_token = sessions.create_login_session(user_db.inserted_id)
    if SignupConfig.enable_welcome_email:
        send_email(
            "WelcomeEmail",
            signup_model.email,
            **signup_model.model_dump(exclude={"password"})
        )
    return LoginResponse(session_token=session_token)
