from typing import Generator

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_token(request: Request) -> str:
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param


def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    token = get_token(request)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        id = payload.get("sub")
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_kakao_user(code: schemas.Code) -> schemas.KakaoUser:
    get_access_token_headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    params = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_APP_KEY,
        "redirect_uri": code.redirect_uri,
        "code": code.code,
    }

    kakao_access_token = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers=get_access_token_headers,
        params=params,
    ).json()
    if not kakao_access_token.get("access_token"):
        raise HTTPException(status_code=401, detail="Incorrect code")

    get_user_info_headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        "Authorization": "Bearer " + kakao_access_token["access_token"],
    }

    kakao_user = requests.post(
        "https://kapi.kakao.com/v2/user/me", headers=get_user_info_headers
    ).json()

    if not kakao_user.get("id"):
        raise HTTPException(status_code=500, detail="Get kakao id error")

    return kakao_user
