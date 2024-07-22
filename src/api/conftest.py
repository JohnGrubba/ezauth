import pytest
import datetime
import uuid
import bcrypt
from tools import users_collection, sessions_collection


@pytest.fixture
def fixtureuser() -> dict:
    users_collection.find_one_and_delete({"email": "fixtureuser@gmail.com"})
    hashed_pswd = bcrypt.hashpw("Kennwort1!".encode("utf-8"), bcrypt.gensalt(5)).decode(
        "utf-8"
    )
    user_data = {
        "password": hashed_pswd,
        "email": "fixtureuser@gmail.com",
        "username": "FixtureUser",
        "createdAt": datetime.datetime.now(),
        "test": True,
    }
    result = users_collection.insert_one(user_data)
    user_data["password"] = "Kennwort1!"
    user_data["_id"] = str(result.inserted_id)
    return user_data


@pytest.fixture
def fixturesessiontoken_user(fixtureuser) -> tuple[str, dict]:
    # Generate a new session token
    session_token = str(uuid.uuid4())
    # Persist the session
    sessions_collection.insert_one(
        {
            "session_token": session_token,
            "user_id": fixtureuser["_id"],
            "createdAt": datetime.datetime.now(),
        }
    )
    return session_token, fixtureuser
