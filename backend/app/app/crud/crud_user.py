from random import randint
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import create_uuid, get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        if not obj_in.password:
            obj_in.password = create_uuid()
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            id=create_uuid(),
            is_superuser=obj_in.is_superuser,
            color_id=randint(0, 9),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        update_data["is_active"] = True
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):  # type: ignore
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def get_by_kakao_id(self, db: Session, *, kakao_id: int) -> Optional[User]:
        return db.query(User).filter(User.kakao_id == kakao_id).first()

    def create_by_kakao_id(
        self, db: Session, *, kakao_id: int, nickname: Optional[str]
    ) -> User:
        db_obj = User(
            id=create_uuid(),
            kakao_id=kakao_id,
            hashed_password=get_password_hash(create_uuid()),
            nickname=nickname,
            color_id=randint(0, 9),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
