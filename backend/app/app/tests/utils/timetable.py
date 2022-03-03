from sqlalchemy.orm import Session

from app import crud
from app.models.timetable import TimeTable
from app.schemas.timetable import TimeTableCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_timetable(db: Session) -> TimeTable:

    user = create_random_user(db)
    title = random_lower_string()
    description = random_lower_string()
    timetable_in = TimeTableCreate(title=title, description=description)
    timetable = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=user.id
    )

    return timetable
