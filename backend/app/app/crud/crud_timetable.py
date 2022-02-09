from sqlalchemy.orm import Session

from app.core.security import create_uuid
from app.crud.base import CRUDBase
from app.models.timetable import TimeTable
from app.schemas.timetable import TimeTableCreate, TimeTableUpdate


class CRUDTimeTable(CRUDBase[TimeTable, TimeTableCreate, TimeTableUpdate]):
    def create(
        self, db: Session, *, obj_in: TimeTableCreate, user_id: str
    ) -> TimeTable:
        db_obj = TimeTable(
            id=create_uuid(),
            title=obj_in.title,
            description=obj_in.description,
            create_user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


timetable = CRUDTimeTable(TimeTable)
