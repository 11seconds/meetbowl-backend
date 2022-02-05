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
            start_time=obj_in.start_time,
            end_time=obj_in.end_time,
            day=obj_in.day,
            label=obj_in.label
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    
    def get_all(self, db:Session, table_id:str):
        db_obj = db.query(
            self.model.user_id,
            self.model.start_time,
            self.model.end_time).filter(self.model.table_id==table_id).all()
        return db_obj
    
    def get_all_by_user_id(self, db:Session, table_id:str, user_id:str):
        db_obj = db.query(
            self.model.user_id,
            self.model.start_time,
            self.model.end_time).filter(self.model.table_id==table_id, self.model.user_id==user_id).all()
        return db_obj

scheduleblock = CRUDScheduleblock(ScheduleBlock)
