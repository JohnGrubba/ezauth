from pydantic import BaseModel, field_validator, EmailStr, SecretStr, ConfigDict, Field
from typing import Optional, List
from tools import SignupConfig
import re
import bcrypt


class InternalUserQuery(BaseModel):
    query: dict
    sort: dict
    page: int = 0


class SessionDetailResponse(BaseModel):
    id: str = Field(alias="_id")
    device_information: dict
    createdAt: str


class SessionListResponseModel(BaseModel):
    sessions: List[SessionDetailResponse]


class ConfirmationCode(BaseModel):
    code: int | str


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


class ConfirmEmailCodeRequest(ConfirmationCode):
    identifier: str


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
        if len(pswd) == 0:
            raise ValueError("Password cannot be empty")
        if len(pswd) < 8 and SignupConfig.password_complexity >= 1:
            raise ValueError("Make sure your password has at least 8 letters")
        elif re.search("[0-9]", pswd) is None and SignupConfig.password_complexity >= 2:
            raise ValueError("Make sure your password has a number in it")
        elif re.search("[A-Z]", pswd) is None and SignupConfig.password_complexity >= 3:
            raise ValueError("Make sure your password has a capital letter in it")
        elif (
            re.search("[^a-zA-Z0-9]", pswd) is None
            and SignupConfig.password_complexity >= 4
        ):
            raise ValueError("Make sure your password has a special character in it")
        elif len(pswd) > 50:
            raise ValueError("Make sure your password is at most 50 characters")
        # Hash Password
        hashed_pswd = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt(10)).decode(
            "utf-8"
        )
        return hashed_pswd


class DeleteAccountRequest(BaseModel):
    password: SecretStr


class ResetPasswordRequest(PasswordHashed):
    identifier: str


class UserSignupRequest(PasswordHashed):
    email: EmailStr
    username: str

    model_config = ConfigDict(
        extra="allow",
    )

    @field_validator("username")
    @classmethod
    def username_check(cls, username: str) -> str:
        if len(username) == 0:
            raise ValueError("Username cannot be empty")
        if len(username) < 4:
            if SignupConfig.username_complexity >= 1:
                raise ValueError("Username must be at least 4 characters long")
        if len(username) > 20:
            if SignupConfig.username_complexity >= 2:
                raise ValueError("Username must be at most 20 characters long")
        elif re.search("[^a-zA-Z0-9]", username) is not None:
            raise ValueError("Username must only contain letters and numbers")
        return username
