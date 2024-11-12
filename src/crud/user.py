from crud import sessions
from tools import (
    users_collection,
    SignupConfig,
    queue_email,
    InternalConfig,
    insecure_cols,
    AccountFeaturesConfig,
    default_signup_fields,
    case_insensitive_collation,
    all_ids,
    regenerate_ids,
    r,
)
from fastapi import HTTPException, BackgroundTasks, Request
from api.model import UserSignupRequest, InternalUserCreateRequest
import pymongo
from typing import List
import bson
import datetime
import json
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


def change_email(user_id: str, new_email: str) -> None:
    """Change the email of a user

    Args:
        user_id (str): User ID
        new_email (str): New Email
    """
    # Retrieve the existing user data
    users_collection.update_one(
        {"_id": bson.ObjectId(user_id)}, {"$set": {"email": new_email}}
    )


def update_public_user(
    user_id: str, data: dict, background_tasks: BackgroundTasks, internal: bool = False
) -> dict:
    """Updates Public User Data

    Args:
        user_id (str): User ID
        data (dict): Data to Update
    """
    # Retrieve the existing user data
    existing_user = users_collection.find_one({"_id": bson.ObjectId(user_id)})
    # Allow update of all columns except InternalConfig.internal_columns
    data = {
        k: v
        for k, v in data.items()
        if internal or (k not in InternalConfig.not_updateable_columns)
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

    # Check if username field is set and if user sends different one and if it is already in use
    if (
        data.get("username", "")
        and existing_user["username"].lower() != data.get("username", "").lower()
        and get_user_identifier(data.get("username", ""))
    ):
        raise HTTPException(detail="Username already in use.", status_code=409)
    # Check if email field is set and if user sends different one and if it is already in use
    if data.get("email", "") and existing_user["email"] != data.get("email", ""):
        # Check if someone else has this email already
        if get_user_identifier(data["email"]):
            raise HTTPException(detail="Email already in use.", status_code=409)
        data["email"] = data["email"].lower()

        if r.getex("emailchange:" + str(existing_user["_id"])):
            raise HTTPException(
                detail="Email Change already requested. Please confirm the email change.",
                status_code=409,
            )

        existing_user.pop("password")
        # Send Confirmation E-Mail for new email address
        if not all_ids:
            # Generate new ids
            regenerate_ids()
        # Get a unique ID for confirmation email
        unique_id = all_ids.pop()
        # Generate and send confirmation email
        queue_email(
            "ConfirmEmail",
            data["email"],
            **existing_user,
            code=unique_id,
            time=SignupConfig.conf_code_expiry,
        )
        r.setex(
            "emailchange:" + str(existing_user["_id"]),
            SignupConfig.conf_code_expiry * 60,
            json.dumps({"new-email": data["email"], "code": unique_id}),
        )

        data.pop("email")

    return users_collection.find_one_and_update(
        {"_id": bson.ObjectId(user_id)},
        {"$set": data},
        insecure_cols if internal else InternalConfig.internal_columns,
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


def get_user_identifier(credential: str) -> dict:
    """Get a user by email or username

    Args:
        credential (str): Email or Username

    Returns:
        dict: User Data
    """
    try:
        credential = bson.ObjectId(credential)
    except bson.errors.InvalidId:
        pass
    return users_collection.find_one(
        {
            "$or": [
                {"email": credential},
                {"username": credential},
                {"_id": credential},
            ]
        },
        collation=case_insensitive_collation,
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
                    {"email": email},
                    {"username": username},
                ]
            },
            collation=case_insensitive_collation,
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
        queue_email("WelcomeEmail", data["email"], **data)
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


def bulk_crt_users(usrs: List[InternalUserCreateRequest]) -> None:
    """Bulk Create Users

    Args:
        usrs (List[InternalUserCreateRequest]): List of Users
    """
    usrs = [{**usr.dict(), "createdAt": datetime.datetime.now()} for usr in usrs]
    try:
        users_collection.insert_many(usrs)
    except pymongo.errors.BulkWriteError:
        raise HTTPException(
            detail="Invalid User Data - or Duplicate Entries", status_code=400
        )
