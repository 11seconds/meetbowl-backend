from pydoc import describe
from typing import Any, Dict, Optional, Union, List
from sqlalchemy import table

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.scheduleblock import ScheduleBlock
from app.schemas.scheduleblock import ScheduleBlockCreate, ScheduleBlockUpdate

from app.core.security import create_uuid


class CRUDScheduleblock(CRUDBase[ScheduleBlock, ScheduleBlockCreate, ScheduleBlockUpdate]):
    def create(self, db: Session, *, obj_in: ScheduleBlockCreate, user_id: str) -> ScheduleBlock:
        db_obj = ScheduleBlock(
            id=create_uuid(),
            table_id=obj_in.table_id,
            user_id=user_id,
            start_datetime=obj_in.start_datetime,
            end_datetime=obj_in.end_datetime,
            label=obj_in.label
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_all(self, db: Session, *, objs_in: List[ScheduleBlockCreate], user_id: str) -> List[ScheduleBlock]:
        db_objs = []
        
        for obj in objs_in:
            db_objs.append(
                ScheduleBlock(
                    id=create_uuid(),
                    table_id=obj.table_id,
                    user_id=user_id,
                    start_datetime=obj.start_datetime,
                    end_datetime=obj.end_datetime,
                    label=obj.label
                )
            )
        db.add_all(db_objs)
        db.commit()
        return db_objs
    
    def get_all(self, db:Session, table_id:str):
        db_obj = db.query(self.model.user_id, self.model.start_datetime, self.model.end_datetime).filter(self.model.table_id==table_id).all()
        return db_obj


scheduleblock = CRUDScheduleblock(ScheduleBlock)
