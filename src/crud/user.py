from crud import sessions
from tools import (
    users_collection,
    SignupConfig,
    send_email,
    InternalConfig,
    insecure_cols,
)
from fastapi import HTTPException, BackgroundTasks, Request
from api.model import UserSignupRequest
import pymongo
import bson
import datetime


def link_google_account(user_id: str, google_uid: str) -> None:
    """Link a Google Account to a User

    Args:
        user_id (str): User ID
        google_uid (str): Google UID
    """
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)}, {"$set": {"google_uid": google_uid}}
    )


def get_user_by_google_uid(google_uid: str) -> dict:
    """Get a user by Google UID

    Args:
        google_uid (str): Google UID

    Returns:
        dict: User Data
    """
    return users_collection.find_one({"google_uid": google_uid})


def link_github_account(user_id: str, github_uid: str) -> None:
    """Link a Github Account to a User

    Args:
        user_id (str): User ID
        github_uid (str): Github UID
    """
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)}, {"$set": {"github_uid": github_uid}}
    )


def get_user_by_github_uid(github_uid: str) -> dict:
    """Get a user by Github UID

    Args:
        github_uid (str): Github UID

    Returns:
        dict: User Data
    """
    return users_collection.find_one({"github_uid": github_uid})


def get_batch_users(user_ids: list) -> list:
    """Get a batch of users by ID

    Args:
        user_ids (list): List of User IDs

    Returns:
        list: List of User Data
    """
    try:
        bson_ids = [bson.ObjectId(i) for i in user_ids]
    except bson.errors.InvalidId:
        raise HTTPException(detail="Invalid User ID", status_code=400)
    return list(users_collection.find({"_id": {"$in": bson_ids}}, insecure_cols))


def update_public_user(user_id: str, data: dict) -> None:
    """Updates Public User Data

    Args:
        user_id (str): User ID
        data (dict): Data to Update
    """
    # Allow update of all columns except InternalConfig.internal_columns
    data = {
        k: v for k, v in data.items() if k not in InternalConfig.not_updateable_columns
    }
    return users_collection.find_one_and_update(
        {"_id": bson.ObjectId(user_id)},
        {"$set": data},
        InternalConfig.internal_columns,
        return_document=pymongo.ReturnDocument.AFTER,
    )


def add_2fa(user_id: str, secret: str) -> None:
    """Adds 2FA to a user

    Args:
        user_id (str): User ID
        secret (str): 2FA Secret
    """
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)}, {"$set": {"2fa_secret": secret}}
    )


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


def get_dangerous_user(user_id: str) -> dict:
    """Gets a user by ID

    Args:
        user_id (str): User ID

    Returns:
        dict: User Data
    """
    return users_collection.find_one({"_id": bson.ObjectId(user_id)})


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
    signup_model: UserSignupRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    additional_data: dict = {},
) -> str | HTTPException:
    """Creates a User in the Database

    Args:
        signup_model (UserSignupRequest): User Data

    Returns:
        str: Session Token
    """
    data = {
        **additional_data,
        **(
            signup_model.model_dump()
            if isinstance(signup_model, UserSignupRequest)
            else {}
        ),
        "createdAt": datetime.datetime.now(),
    }
    # Save the Account into the database
    try:
        user_db = users_collection.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(detail="Email or Username already exists.", status_code=409)
    # Drop password from data
    data.pop("password")
    # User Created (Create Session Token and send Welcome Email)
    session_token = sessions.create_login_session(user_db.inserted_id, request)
    if SignupConfig.enable_welcome_email:
        background_tasks.add_task(send_email, "WelcomeEmail", data["email"], **data)
    return session_token
