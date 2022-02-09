from typing import List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import create_uuid
from app.crud.base import CRUDBase
from app.models.scheduleblock import ScheduleBlock
from app.schemas.scheduleblock import ScheduleBlockCreate, ScheduleBlockUpdate


class CRUDScheduleblock(
    CRUDBase[ScheduleBlock, ScheduleBlockCreate, ScheduleBlockUpdate]
):
    def create(
        self, db: Session, *, obj_in: ScheduleBlockCreate, user_id: str
    ) -> ScheduleBlock:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in.start_time not in range(0, 23) or obj_in.end_time not in range(0, 23):
            raise HTTPException(400, detail="Time data must be in 0~23")
        if obj_in.start_minute not in range(0, 59) or obj_in.end_minute not in range(
            0, 59
        ):
            raise HTTPException(400, detail="Minute data must be in 0~59")

        if obj_in.day not in range(0, 6):
            raise HTTPException(
                400, detail="Day data must be in 0~6, 0: Sunday, 6: Saturday"
            )

        db_obj = ScheduleBlock(id=create_uuid(), user_id=user_id, **obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session, table_id: str):
        db_obj = db.query(self.model).filter(self.model.table_id == table_id).all()
        return db_obj

    def get_all_by_user_id(self, db: Session, table_id: str, user_id: str):
        db_obj = (
            db.query(self.model)
            .filter(self.model.table_id == table_id, self.model.user_id == user_id)
            .all()
        )
        return db_obj


scheduleblock = CRUDScheduleblock(ScheduleBlock)
