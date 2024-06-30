from pydantic import BaseModel, field_validator, EmailStr, SecretStr, ConfigDict
import re
import bcrypt


class LoginRequest(BaseModel):
    identifier: str
    password: SecretStr


class LoginResponse(BaseModel):
    session_token: str


class UserSignupRequest(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr

    model_config = ConfigDict(
        extra="allow",
    )

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
