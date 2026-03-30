from typing import Optional
import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    firstName: str
    lastName: str

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """
        Validates that the password meets enterprise security requirements:
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number
        - At least 1 special character
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise ValueError("Password must contain at least one special character")
        return value


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    newPassword: str = Field(..., min_length=8)

    @field_validator("newPassword")
    @classmethod
    def validate_new_password_complexity(cls, value: str) -> str:
        # Reusing the strict logic from registration
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise ValueError("Password must contain at least one special character")
        return value
