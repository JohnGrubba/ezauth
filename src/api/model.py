from pydantic import BaseModel, field_validator, EmailStr, SecretStr, ConfigDict
from typing import Optional
import re
import bcrypt


class TwoFactorAddResponse(BaseModel):
    provision_uri: str


class InternalProfileRequest(BaseModel):
    session_token: Optional[str] = None
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    identifier: str
    password: SecretStr
    two_factor_code: Optional[int] = None


class LoginResponse(BaseModel):
    session_token: str
    expires: int


class ConfirmEmailCodeRequest(BaseModel):
    code: int | str
    email: str


class BroadCastEmailRequest(BaseModel):
    template_name: str
    mongodb_search_condition: dict


class PasswordHashed(BaseModel):
    password: SecretStr

    @field_validator("password")
    @classmethod
    def password_check_hash(cls, password: SecretStr) -> str:
        # Validate Password
        pswd = password.get_secret_value()
        if len(pswd) < 8:
            raise ValueError("Make sure your password is at least 8 letters")
        elif re.search("[0-9]", pswd) is None:
            raise ValueError("Make sure your password has a number in it")
        elif re.search("[A-Z]", pswd) is None:
            raise ValueError("Make sure your password has a capital letter in it")
        elif re.search("[^a-zA-Z0-9]", pswd) is None:
            raise ValueError("Make sure your password has a special character in it")
        # Hash Password
        hashed_pswd = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt(5)).decode(
            "utf-8"
        )
        return hashed_pswd


class UserSignupRequest(PasswordHashed):
    email: EmailStr
    username: str

    model_config = ConfigDict(
        extra="allow",
    )

    @field_validator("username")
    @classmethod
    def username_check(cls, username: str) -> str:
        if len(username) < 4:
            raise ValueError("Username must be at least 4 characters long")
        elif re.search("[^a-zA-Z0-9]", username) is not None:
            raise ValueError("Username must only contain letters and numbers")
        return username
