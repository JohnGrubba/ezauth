from pydantic import BaseModel, field_validator, EmailStr, SecretStr, ConfigDict, Field
from typing import Optional, List
from api.helpers.validators import username_check, password_check_hash


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
    def pswdcheck(cls, password: SecretStr) -> str:
        return password_check_hash(cls, password)


class Username(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def usrchck(cls, username: str) -> str:
        return username_check(cls, username)


class DeleteAccountRequest(BaseModel):
    password: SecretStr


class ResetPasswordRequest(PasswordHashed):
    identifier: str


class UserSignupRequest(PasswordHashed, Username):
    email: EmailStr

    model_config = ConfigDict(
        extra="allow",
    )


class ProfileUpdateRequest(Username):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    model_config = ConfigDict(
        extra="allow",
    )


class InternalUserCreateRequest(Username):
    email: EmailStr

    model_config = ConfigDict(
        extra="allow",
    )
