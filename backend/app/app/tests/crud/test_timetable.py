from sqlalchemy.orm import Session

from app import crud
from app.api.api_v1.endpoints.timetables import get_timetable_by_id
from app.schemas.timetable import TimeTableCreate, TimeTableUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_timetable_with_user_id(db: Session) -> None:
    user = create_random_user(db)
    title = random_lower_string()
    description = random_lower_string()
    timetable_in = TimeTableCreate(title=title, description=description)
    timetable = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=user.id
    )
    assert timetable is not None
    assert timetable.title == title
    assert timetable.description == description


def test_update_timetable(db: Session) -> None:
    user = create_random_user(db)
    title = random_lower_string()
    description = random_lower_string()
    timetable_in = TimeTableCreate(title=title, description=description)
    timetable_db = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=user.id
    )

    updated_title = random_lower_string()
    timetable_in_update = TimeTableUpdate(title=updated_title)
    updated_timetable = crud.timetable.update(
        db, db_obj=timetable_db, obj_in=timetable_in_update
    )

    assert updated_timetable is not None
    assert updated_timetable.title == updated_title


def test_get_timetable(db: Session) -> None:
    user = create_random_user(db)
    title = random_lower_string()
    description = random_lower_string()
    timetable_in = TimeTableCreate(title=title, description=description)
    timetable_db = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=user.id
    )

    get_timetable = crud.timetable.get(db, id=timetable_db.id)

    assert get_timetable
    assert get_timetable is not None
    assert get_timetable.title == timetable_db.title


def test_get_timetables_by_user_id(db: Session) -> None:
    user = create_random_user(db)
    for _ in range(20):
        title = random_lower_string()
        description = random_lower_string()
        timetable_in = TimeTableCreate(title=title, description=description)
        timetable_db = crud.timetable.create_with_user_id(
            db, obj_in=timetable_in, user_id=user.id
        )

    my_timetable = crud.timetable.get_by_user_id(db, user_id=user.id)

    assert my_timetable is not None
    assert len(my_timetable) == 20
    assert my_timetable[0].create_user_id == user.id
