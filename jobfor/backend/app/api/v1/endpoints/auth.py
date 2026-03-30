from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.core.async_database import get_async_db
from app.models.models import User
from app.schemas.auth import (
    RegisterInput,
    LoginInput,
    TokenResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.api.dependencies.auth import get_current_user
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_in: RegisterInput,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Register a new user and create their Profile.
    """
    auth_service = AuthService(db)
    return await auth_service.register(user_in)


@router.post("/login")
async def login(
    login_in: LoginInput,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Login with email and password to receive access and refresh JWTs.
    """
    auth_service = AuthService(db)
    return await auth_service.login(login_in)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Exchange a valid refresh token for a new access/refresh pair.
    """
    auth_service = AuthService(db)
    return await auth_service.refresh_token(refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> None:
    """
    Invalidates the current user's refresh token.
    """
    auth_service = AuthService(db)
    await auth_service.logout(current_user.id)


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieves the currently authenticated user's profile information.
    """
    # Simply return the user from the dependency — no DB lookup needed here
    # as the dependency already fetched it.
    return current_user


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def request_password_reset(
    req: PasswordResetRequest,
    db: AsyncSession = Depends(get_async_db)
) -> dict:
    """
    Provisions a password reset token and simulates email dispatch.
    Always returns 202 to prevent email enumeration.
    """
    auth_service = AuthService(db)
    await auth_service.request_password_reset(req.email)
    return {"msg": "If that email is registered, a reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    req: PasswordResetConfirm,
    db: AsyncSession = Depends(get_async_db)
) -> dict:
    """
    Verifies a reset token and sets a new password.
    """
    auth_service = AuthService(db)
    await auth_service.reset_password(req.token, req.newPassword)
    return {"msg": "Password updated successfully."}


# ── OAuth Placeholders ──────────────────────────────────────────

@router.get("/google")
async def auth_google() -> dict:
    """
    Placeholder: Start Google OAuth2 Flow
    """
    return {"msg": "Google OAuth redirect flow not implemented"}


@router.get("/github")
async def auth_github() -> dict:
    """
    Placeholder: Start GitHub OAuth2 Flow
    """
    return {"msg": "GitHub OAuth redirect flow not implemented"}
