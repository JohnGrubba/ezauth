from crud import sessions
from tools import (
    users_collection,
    SignupConfig,
    send_email,
    InternalConfig,
    insecure_cols,
    AccountFeaturesConfig,
    default_signup_fields,
)
from fastapi import HTTPException, BackgroundTasks, Request
from api.model import UserSignupRequest
import pymongo
import bson
import datetime
from crud.sessions import clear_sessions_for_user


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
    # Retrieve the existing user data
    existing_user = users_collection.find_one({"_id": bson.ObjectId(user_id)})
    # Allow update of all columns except InternalConfig.internal_columns
    data = {
        k: v for k, v in data.items() if k not in InternalConfig.not_updateable_columns
    }

    if AccountFeaturesConfig.allow_add_fields_patch_user:
        data = {
            k: v
            for k, v in data.items()
            if k in AccountFeaturesConfig.allow_add_fields_patch_user
            or k in existing_user
        }
    else:
        data = {k: v for k, v in data.items() if k in existing_user}

    # Check if username in use
    if data.get("username", "") and get_user_email_or_username(
        data.get("username", "")
    ):
        raise HTTPException(detail="Username already in use.", status_code=409)

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
        {
            "$or": [
                {"email": {"$regex": credential, "$options": "i"}},
                {"username": {"$regex": credential, "$options": "i"}},
            ]
        }
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
        users_collection.find_one(
            {
                "$or": [
                    {"email": {"$regex": email, "$options": "i"}},
                    {"username": {"$regex": username, "$options": "i"}},
                ]
            }
        )
        is not None
    )


def create_user(
    signup_model: UserSignupRequest | dict,
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
    if isinstance(signup_model, UserSignupRequest):
        if AccountFeaturesConfig.allow_add_fields_on_signup:
            dmp = signup_model.model_dump(
                include=default_signup_fields
                | AccountFeaturesConfig.allow_add_fields_on_signup,
            )
        else:
            # Only Dump Required Fields
            dmp = signup_model.model_dump(include=default_signup_fields)
    else:
        # Input is a dictionary (from redis maybe)
        # Only dump default_signup_fields
        dmp = {k: v for k, v in signup_model.items() if k in default_signup_fields}

    data = {
        **additional_data,
        **dmp,
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


def remove_user(user_id: str) -> None:
    """Remove a User from the Database

    Args:
        user_id (str): User ID
    """
    users_collection.delete_one({"_id": bson.ObjectId(user_id)})
    clear_sessions_for_user(user_id)


def schedule_delete_user(user_id: str) -> None:
    """Schedule a User for Deletion

    Args:
        user_id (str): User ID
    """
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)},
        {
            "$set": {
                "expiresAfter": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(
                    minutes=AccountFeaturesConfig.deletion_pending_minutes
                )
            }
        },
    )
    clear_sessions_for_user(user_id)


def query_users(query: dict, sort: dict, page: 0) -> list:
    """Query Users based on a query string

    Args:
        query (str): Query String

    Returns:
        list: List of User Data
    """
    max_results = 100
    return list(
        users_collection.find(query, sort=sort)
        .skip(page * max_results)
        .limit(max_results)
    )


def restore_usr(user_id: str) -> None:
    """Restore a User from Deletion

    Args:
        user_id (str): User ID
    """
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)}, {"$unset": {"expiresAfter": ""}}
    )


def count_users() -> int:
    """Count the number of users

    Returns:
        int: Number of Users
    """
    return users_collection.count_documents({})


def count_oauth() -> dict:
    """Count the number of users

    Returns:
        dict: Number of Users
    """
    return {
        "google_oauth_count": users_collection.count_documents(
            {"google_uid": {"$exists": True}}
        ),
        "github_oauth_count": users_collection.count_documents(
            {"github_uid": {"$exists": True}}
        ),
    }
