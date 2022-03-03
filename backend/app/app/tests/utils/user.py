from datetime import timedelta
from typing import Dict

from sqlalchemy.orm import Session

from app import crud
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def get_auth_header(*, user_id: str) -> Dict[str, str]:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    auth_token = security.create_access_token(
        user_id, expires_delta=access_token_expires
    )
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user
