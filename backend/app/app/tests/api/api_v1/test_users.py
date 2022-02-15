from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.user import get_auth_header


def test_get_me(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    auth_header = get_auth_header(user_id=user_id)

    r = client.get(f"{settings.API_V1_STR}/users/me", headers=auth_header)
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_patch_user_me(client: TestClient, db: Session) -> None:
    username = random_email()
    user_in = UserCreate(email=username)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    auth_header = get_auth_header(user_id=user_id)

    nickname = random_lower_string()
    data = {"nickname": nickname}
    r = client.patch(f"{settings.API_V1_STR}/users/me", headers=auth_header, json=data)
    assert 200 <= r.status_code < 300


def test_patch_user_me_empty_nickname(client: TestClient, db: Session) -> None:
    username = random_email()
    user_in = UserCreate(email=username)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    auth_header = get_auth_header(user_id=user_id)

    nickname = ""
    data = {"nickname": nickname}
    r = client.patch(f"{settings.API_V1_STR}/users/me", headers=auth_header, json=data)

    assert r.status_code == 400

