from random import randint

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    user_in = UserCreate(email=email)
    user = crud.user.create(db, obj_in=user_in)
    assert user
    assert user.email == email


def test_create_user_by_kakao_id(db: Session) -> None:
    kakao_id = randint(1000000, 9999999)
    nickname = random_lower_string()
    user = crud.user.create_by_kakao_id(db, kakao_id=kakao_id, nickname=nickname)
    assert user
    assert user.kakao_id == kakao_id
    assert user.nickname == nickname


def test_get_user_by_kakao_id(db: Session) -> None:
    kakao_id = randint(1000000, 9999999)
    nickname = random_lower_string()
    user = crud.user.create_by_kakao_id(db, kakao_id=kakao_id, nickname=nickname)
    get_user = crud.user.get_by_kakao_id(db, kakao_id=kakao_id)
    assert get_user
    assert user == get_user
    assert get_user.kakao_id == kakao_id


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    get_user = crud.user.get(db, id=user.id)
    assert get_user
    assert user.email == get_user.email
    assert jsonable_encoder(user) == jsonable_encoder(get_user)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=False)
    user = crud.user.create(db, obj_in=user_in)
    new_nickname = random_lower_string()
    user_in_update = UserUpdate(nickname=new_nickname, is_superuser=True)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user_2 is not None
    assert user.email == user_2.email
    assert user.nickname == user_2.nickname
