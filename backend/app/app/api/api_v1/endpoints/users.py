from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/users/login", response_model=schemas.Token)
def user_kakao(
    *,
    db: Session = Depends(deps.get_db),
    kakao_user: schemas.KakaoUser = Depends(deps.get_kakao_user),
) -> Any:

    user = crud.user.get_by_kakao_id(db, kakao_id=kakao_user.get("id"))

    if user:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = schemas.Token(
            access_token=security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            token_type="bearer",
        )

        return access_token

    created_user = crud.user.create_by_kakao_id(
        db, kakao_id=kakao_user.get("id"), nickname="",
    )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = schemas.Token(
        access_token=security.create_access_token(
            created_user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

    return access_token


@router.get("/users/me", response_model=schemas.User)
def get_user_me(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    본인 유저 정보 조회

    JWT 필요
    """
    return current_user


@router.patch("/users/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
    user_in: schemas.UserUpdate,
) -> Any:
    """
    본인 유저 정보 수정

    JWT 필요
    """

    if user_in.nickname is not None and user_in.nickname == "":
        raise HTTPException(status_code=400, detail="Nickname must not be empty string")

    user_db = crud.user.get(db, id=current_user.id)

    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud.user.update(db, db_obj=user_db, obj_in=user_in)

    return updated_user
