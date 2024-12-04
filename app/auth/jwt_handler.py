import os
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="token",
    tokenUrl="token",
)


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except JWTError:
        raise credentials_exception
    return token_data


def get_user_with_read_access(current_user: TokenData = Depends(get_current_user)):
    if "course_service:read" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user


def get_user_with_write_access(current_user: TokenData = Depends(get_current_user)):
    if "course_service:write" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user
