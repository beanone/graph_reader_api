import logging
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

LOCKSMITHA_URL = os.getenv("LOCKSMITHA_URL", "http://localhost:8001")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{LOCKSMITHA_URL}/auth/jwt/login")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")  # Should match Locksmitha's secret
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

logger = logging.getLogger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
