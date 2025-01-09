from tools import SignupConfig
import re
import bcrypt
from pydantic import SecretStr


def username_check(cls, username: str) -> str:
    if len(username) == 0:
        raise ValueError("Username cannot be empty")
    if len(username) < 4:
        if SignupConfig.username_complexity >= 1:
            raise ValueError("Username must be at least 4 characters long")
    if len(username) > 20:
        if SignupConfig.username_complexity >= 2:
            raise ValueError("Username must be at most 20 characters long")

    # Additional Regex Checks
    if re.search(SignupConfig.username_regex, username) is not None:
        raise ValueError("Username must only contain letters and numbers")

    # Blocklist Check
    if username.lower() in SignupConfig.username_blocklist:
        raise ValueError("Username is not allowed")

    return username


def password_check_hash(cls, password: SecretStr) -> str:
    # Validate Password
    pswd = password.get_secret_value()
    if len(pswd) == 0:
        raise ValueError("Password cannot be empty")
    if len(pswd) < 8 and SignupConfig.password_complexity >= 1:
        raise ValueError("Make sure your password has at least 8 letters")
    if re.search("[0-9]", pswd) is None and SignupConfig.password_complexity >= 2:
        raise ValueError("Make sure your password has a number in it")
    if re.search("[A-Z]", pswd) is None and SignupConfig.password_complexity >= 3:
        raise ValueError("Make sure your password has a capital letter in it")
    if (
        re.search("[^a-zA-Z0-9]", pswd) is None
        and SignupConfig.password_complexity >= 4
    ):
        raise ValueError("Make sure your password has a special character in it")
    if len(pswd) > 50:
        raise ValueError("Make sure your password is at most 50 characters")

    # Additional Regex Checks
    if re.search(SignupConfig.password_regex, pswd) is not None:
        raise ValueError("Password does not meet complexity requirements")

    # Hash Password
    hashed_pswd = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt(10)).decode(
        "utf-8"
    )
    return hashed_pswd
