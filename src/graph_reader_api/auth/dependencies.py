import logging
import os
from datetime import UTC

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from keylin.db import get_async_session
from keylin.keylin_utils import hash_api_key
from keylin.models import APIKey, User
from sqlalchemy import select

# Add these imports for keylin integration
from sqlalchemy.ext.asyncio import AsyncSession

LOCKSMITHA_URL = os.getenv("LOCKSMITHA_URL", "http://localhost:8001")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{LOCKSMITHA_URL}/auth/jwt/login")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")  # Should match Locksmitha's secret
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

logger = logging.getLogger(__name__)

API_KEY_HEADER = "X-API-Key"
API_KEY_QUERY = "api_key"


async def get_api_key_from_request(request: Request) -> str | None:
    api_key = request.headers.get(API_KEY_HEADER)
    if api_key:
        return api_key
    api_key = request.query_params.get(API_KEY_QUERY)
    return api_key


async def validate_api_key_local(api_key: str, session: AsyncSession) -> dict:
    from datetime import datetime

    key_hash = hash_api_key(api_key)
    stmt = select(APIKey).where(APIKey.key_hash == key_hash, APIKey.status == "active")
    result = await session.execute(stmt)
    api_key_obj = result.scalar_one_or_none()
    if api_key_obj is None:
        logger.warning("API key not found or invalid.")
        raise HTTPException(status_code=401, detail="Invalid API key")
    # Optionally check expiry
    if api_key_obj.expires_at is not None and api_key_obj.expires_at < datetime.now(
        UTC
    ):
        logger.warning("API key expired.")
        raise HTTPException(status_code=401, detail="API key expired")
    # Get user info
    user_result = await session.execute(
        select(User).where(User.id == api_key_obj.user_id)
    )
    user = user_result.scalar_one_or_none()
    return {
        "sub": api_key_obj.user_id,
        "email": user.email if user else None,
        "api_key_id": api_key_obj.id,
    }


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    api_key = await get_api_key_from_request(request)
    if api_key:
        # Prefer API key if present
        user_info = await validate_api_key_local(api_key, session)
        return user_info
    # Fallback to JWT
    logger.debug(f"Received token: {token}")
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[ALGORITHM], audience="fastapi-users:auth"
        )
        user_id = payload.get("sub")
        if user_id is None:
            logger.warning("Token missing 'sub' claim.")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.debug(f"Token payload: {payload}")
        return payload
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token") from None
