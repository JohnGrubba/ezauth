from crud import sessions
from tools import (
    users_collection,
    SignupConfig,
    send_email,
    InternalConfig,
    insecure_cols,
)
from fastapi import HTTPException, BackgroundTasks, Response
from api.model import UserSignupRequest, LoginResponse
import pymongo, bson
import datetime


def change_pswd(user_id: str, new_password: str) -> None:
    """Changes the password of a user

    Args:
        user_id (str): User ID
        new_password (str): New Password
    """
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)},
        {"$set": {"password": new_password}},
    )


def get_user(user_id: str) -> dict:
    """Gets a user by ID

    Args:
        user_id (str): User ID

    Returns:
        dict: User Data
    """
    return users_collection.find_one({"_id": bson.ObjectId(user_id)}, insecure_cols)


def get_public_user(user_id: str) -> dict:
    """Gets public columns of a user

    Args:
        user_id (str): User ID

    Returns:
        dict: Public User Data
    """
    return users_collection.find_one(
        {"_id": bson.ObjectId(user_id)}, InternalConfig.internal_columns
    )


def get_user_email_or_username(credential: str) -> dict:
    """Get a user by email or username

    Args:
        credential (str): Email or Username

    Returns:
        dict: User Data
    """
    return users_collection.find_one(
        {"$or": [{"email": credential}, {"username": credential}]}
    )


def check_unique_usr(email: str, username: str) -> bool:
    """Check if the email or username is already in use

    Args:
        email (str): Email
        username (str): Username

    Returns:
        bool: True if email or username is already in use
    """
    return (
        users_collection.find_one({"$or": [{"email": email}, {"username": username}]})
        is not None
    )


def create_user(
    signup_model: UserSignupRequest, background_tasks: BackgroundTasks
) -> str | HTTPException:
    """Creates a User in the Database

    Args:
        signup_model (UserSignupRequest): User Data

    Returns:
        str: Session Token
    """
    # Save the Account into the database
    try:
        user_db = users_collection.insert_one(
            {**signup_model.model_dump(), "createdAt": datetime.datetime.now()}
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(detail="Email or Username already exists.", status_code=409)
    # User Created (Create Session Token and send Welcome Email)
    session_token = sessions.create_login_session(user_db.inserted_id)
    if SignupConfig.enable_welcome_email:
        background_tasks.add_task(
            send_email,
            "WelcomeEmail",
            signup_model.email,
            **signup_model.model_dump(exclude={"password"})
        )
    return session_token
