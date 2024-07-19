import pytest
import datetime
import bcrypt
from tools import users_collection


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
    }
    users_collection.insert_one(user_data)
    user_data["password"] = "Kennwort1!"
    return user_data
