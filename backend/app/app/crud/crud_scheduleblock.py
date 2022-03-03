from typing import List, Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import create_uuid
from app.crud.base import CRUDBase
from app.models.color import Color
from app.models.scheduleblock import ScheduleBlock
from app.models.user import User
from app.schemas.scheduleblock import ScheduleBlockCreate, ScheduleBlockUpdate


class CRUDScheduleblock(
    CRUDBase[ScheduleBlock, ScheduleBlockCreate, ScheduleBlockUpdate]
):
    def create_with_user_id(
        self, db: Session, *, obj_in: ScheduleBlockCreate, user_id: str
    ) -> ScheduleBlock:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in.start_time not in range(0, 24) or obj_in.end_time not in range(0, 24):
            raise HTTPException(400, detail="Time data must be in 0~23")
        if obj_in.start_minute not in range(0, 60) or obj_in.end_minute not in range(
            0, 60
        ):
            raise HTTPException(400, detail="Minute data must be in 0~59")

        if obj_in.day not in range(0, 7):
            raise HTTPException(
                400, detail="Day data must be in 0~6, 0: Sunday, 6: Saturday"
            )

        db_obj = ScheduleBlock(id=create_uuid(), user_id=user_id, **obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session, table_id: str) -> List[ScheduleBlock]:
        db_obj = (
            db.query(
                self.model.id,
                self.model.start_time,
                self.model.start_minute,
                self.model.end_time,
                self.model.end_minute,
                self.model.day,
                self.model.label,
                self.model.user_id,
                self.model.table_id,
                Color.hex.label("color"),
                User.nickname,
            )
            .outerjoin(self.model.user)
            .outerjoin(User.color)
            .filter(self.model.table_id == table_id)
            .all()
        )
        return db_obj

    def get_all_by_user_id(
        self, db: Session, table_id: str, user_id: str
    ) -> List[ScheduleBlock]:
        db_obj = (
            db.query(
                self.model.id,
                self.model.start_time,
                self.model.start_minute,
                self.model.end_time,
                self.model.end_minute,
                self.model.day,
                self.model.label,
                self.model.user_id,
                self.model.table_id,
                Color.hex.label("color"),
                User.nickname,
            )
            .outerjoin(self.model.user)
            .outerjoin(User.color)
            .filter(self.model.table_id == table_id, User.id == user_id)
            .all()
        )
        return db_obj

    def create_all_by_user_id(
        self, db: Session, table_id: str, user_id: str
    ) -> List[ScheduleBlock]:
        db_objs = [
            ScheduleBlock(
                id=create_uuid(),
                table_id=table_id,
                user_id=user_id,
                start_time=start_time,
                start_minute=0,
                end_time=start_time,
                end_minute=59,
                day=day,
            )
            for day, start_time in [
                [day, start_time] for day in range(7) for start_time in range(24)
            ]
        ]

        db.add_all(db_objs)
        db.commit()
        db_obj = (
            db.query(
                self.model.id,
                self.model.start_time,
                self.model.start_minute,
                self.model.end_time,
                self.model.end_minute,
                self.model.day,
                self.model.label,
                self.model.user_id,
                self.model.table_id,
                Color.hex.label("color"),
                User.nickname,
            )
            .outerjoin(self.model.user)
            .outerjoin(User.color)
            .filter(self.model.table_id == table_id, User.id == user_id)
            .all()
        )
        return db_obj

    def delete_all_by_user_id(self, db: Session, table_id: str, user_id: str):
        db_obj = (
            db.query(self.model)
            .filter(self.model.table_id == table_id, self.model.user_id == user_id)
            .delete()
        )

        db.commit()

        return db_obj


scheduleblock = CRUDScheduleblock(ScheduleBlock)
