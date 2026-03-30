import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.models.models import User, Profile
from app.schemas.auth import RegisterInput, LoginInput, TokenResponse
from app.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)


logger = logging.getLogger(__name__)


def hash_reset_token(token: str) -> str:
    """Creates a SHA-256 hash of a plaintext token for fast database lookups."""
    return hashlib.sha256(token.encode()).hexdigest()


class AuthService:
    """
    Handles all authentication and user identity business logic.
    Provides encapsulated, asynchronous methods.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _generate_tokens(self, user: User) -> TokenResponse:
        """Helper to generate JWTs and return a standard TokenResponse schema."""
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        # Save refresh token to user for stateful revocation (optional but secure)
        user.refresh_token = refresh_token
        await self.db.commit()
        
        return TokenResponse(
            accessToken=access_token,
            refreshToken=refresh_token,
        )

    async def register(self, user_in: RegisterInput) -> dict:
        """
        Registers a new user and creates their associated Profile.
        Raises HTTP 409 if the email is already taken.
        """
        # 1. Check if email already exists
        cursor = await self.db.execute(select(User).where(User.email == user_in.email))
        if cursor.scalars().first() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email address is already in use.",
            )

        # 2. Hash password and create User
        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            password_hash=hashed_password,
        )

        # We add the user to session to execute cascading inserts, 
        # but we need the user.id generated first sometimes.
        self.db.add(new_user)
        await self.db.flush() # Flushes DB to get the new_user.id
        
        # 3. Create associated Profile
        new_profile = Profile(
            user_id=new_user.id,
            first_name=user_in.firstName,
            last_name=user_in.lastName,
        )
        self.db.add(new_profile)
        
        # 4. Generate JWTs (will commit to DB internally)
        tokens = await self._generate_tokens(new_user)
        
        return {
            "user": new_user,
            "tokens": tokens
        }

    async def login(self, login_in: LoginInput) -> dict:
        """
        Authenticates a user by email and password. Returns user and tokens.
        """
        # 1. Find User by Email
        cursor = await self.db.execute(select(User).where(User.email == login_in.email))
        user = cursor.scalars().first()

        # 2. Verify existence and password
        if not user or not user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
            
        if not verify_password(login_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
            
        # 3. Update last login and generate tokens
        user.last_login = datetime.now(timezone.utc)
        tokens = await self._generate_tokens(user)
        
        return {
            "user": user,
            "tokens": tokens
        }

    async def refresh_token(self, token: str) -> TokenResponse:
        """
        Validates the refresh token and provisions a new token pair.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Verify against DB state for revocation
        user_id_int = int(user_id)
        user = await self.db.get(User, user_id_int)
        
        if not user or user.refresh_token != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token invalidated or expired. Please login again.",
            )
            
        # Rotating refresh token
        return await self._generate_tokens(user)

    async def logout(self, user_id: int) -> None:
        """
        Nullifies the refresh token. Assumes the access token gracefully expires.
        """
        user = await self.db.get(User, user_id)
        if user:
            user.refresh_token = None
            await self.db.commit()

    async def request_password_reset(self, email: str) -> None:
        """
        Generates a 32-byte secure token. Stores its hash and expiration.
        Simulates sending an email via logs.
        """
        cursor = await self.db.execute(select(User).where(User.email == email))
        user = cursor.scalars().first()
        
        if not user:
            # Silent fallback to prevent email enumeration attacks
            return
            
        # Generate token
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hash_reset_token(raw_token)
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        
        # Save to user
        user.reset_token = hashed_token
        user.reset_token_expires_at = expiration
        await self.db.commit()
        
        logger.info(f"Faux Email Transport: Password reset link for {email} -> https://jobfor.ai/reset/{raw_token}")

    async def reset_password(self, token: str, new_password: str) -> bool:
        """
        Validates the plain token against the hash in the database, 
        and updates the password.
        """
        hashed_token = hash_reset_token(token)
        
        cursor = await self.db.execute(select(User).where(User.reset_token == hashed_token))
        user = cursor.scalars().first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid reset token.")
            
        if user.reset_token_expires_at and user.reset_token_expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Reset token has expired.")
            
        # Hash new password
        user.password_hash = get_password_hash(new_password)
        
        # Clear reset tokens
        user.reset_token = None
        user.reset_token_expires_at = None
        
        # Invalidate current session
        user.refresh_token = None
        
        await self.db.commit()
        return True
