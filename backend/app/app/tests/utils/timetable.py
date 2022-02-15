from typing import Dict
from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core import security
from app.models.timetable import TimeTable
from app.schemas import Token
from app.schemas.timetable import TimeTableCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.user import create_random_user


def create_random_timetable(db: Session) -> TimeTable:

    user = create_random_user(db)
    title = random_lower_string()
    description = random_lower_string()
    timetable_in = TimeTableCreate(title=title, description=description)
    timetable = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=user.id
    )

    return timetable
