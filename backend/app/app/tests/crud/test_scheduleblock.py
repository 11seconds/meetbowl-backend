import pytest
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.scheduleblock import ScheduleBlockCreate
from app.tests.utils.timetable import create_random_timetable
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_scheduleblock_with_user_id(db: Session) -> None:

    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=23,
        start_minute=59,
        end_time=1,
        end_minute=59,
        day=6,
        label=random_lower_string(),
    )

    scheduleblock = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in, user_id=user.id
    )

    assert scheduleblock is not None


def test_create_scheduleblock_with_user_id_time_range_edge(db: Session) -> None:
    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=23,
        start_minute=0,
        end_time=1,
        end_minute=0,
        day=1,
        label=random_lower_string(),
    )

    scheduleblock = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in, user_id=user.id
    )

    assert scheduleblock is not None


def test_create_scheduleblock_with_user_id_time_range_exception(db: Session) -> None:
    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=24,
        start_minute=0,
        end_time=1,
        end_minute=0,
        day=1,
        label=random_lower_string(),
    )

    with pytest.raises(HTTPException):
        scheduleblock = crud.scheduleblock.create_with_user_id(
            db, obj_in=scheduleblock_in, user_id=user.id
        )


def test_create_scheduleblock_with_user_id_minute_range_exception(db: Session) -> None:
    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=4,
        start_minute=60,
        end_time=5,
        end_minute=60,
        day=1,
        label=random_lower_string(),
    )
    with pytest.raises(HTTPException):
        scheduleblock = crud.scheduleblock.create_with_user_id(
            db, obj_in=scheduleblock_in, user_id=user.id
        )


def test_create_scheduleblock_with_user_id_day_range_exception(db: Session) -> None:
    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=4,
        start_minute=50,
        end_time=5,
        end_minute=50,
        day=8,
        label=random_lower_string(),
    )
    with pytest.raises(HTTPException):
        scheduleblock = crud.scheduleblock.create_with_user_id(
            db, obj_in=scheduleblock_in, user_id=user.id
        )


def test_get_all(db: Session) -> None:
    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in_1 = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=0,
        start_minute=0,
        end_time=1,
        end_minute=59,
        day=1,
        label=random_lower_string(),
    )

    scheduleblock_in_2 = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=2,
        start_minute=0,
        end_time=3,
        end_minute=59,
        day=2,
        label=random_lower_string(),
    )

    scheduleblock_in_3 = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=0,
        start_minute=0,
        end_time=5,
        end_minute=0,
        day=6,
        label=random_lower_string(),
    )

    scheduleblock_1 = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in_1, user_id=user.id
    )

    scheduleblock_2 = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in_2, user_id=user.id
    )

    scheduleblock_3 = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in_3, user_id=user.id
    )

    scheduleblocks = crud.scheduleblock.get_all(db, table_id=timetable.id)

    assert scheduleblock_1 is not None
    assert scheduleblock_2 is not None
    assert scheduleblock_3 is not None
    assert jsonable_encoder(scheduleblocks)


def test_get_all_by_user_id(db: Session) -> None:
    timetable = create_random_timetable(db)
    user = create_random_user(db)
    scheduleblock_in_1 = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=0,
        start_minute=0,
        end_time=1,
        end_minute=59,
        day=1,
        label=random_lower_string(),
    )

    scheduleblock_in_2 = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=2,
        start_minute=0,
        end_time=3,
        end_minute=59,
        day=2,
        label=random_lower_string(),
    )

    scheduleblock_in_3 = ScheduleBlockCreate(
        table_id=timetable.id,
        start_time=0,
        start_minute=0,
        end_time=5,
        end_minute=0,
        day=6,
        label=random_lower_string(),
    )

    scheduleblock_1 = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in_1, user_id=user.id
    )

    scheduleblock_2 = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in_2, user_id=user.id
    )

    scheduleblock_3 = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in_3, user_id=user.id
    )

    scheduleblocks = crud.scheduleblock.get_all_by_user_id(
        db, table_id=timetable.id, user_id=user.id
    )

    assert scheduleblock_1 is not None
    assert scheduleblock_2 is not None
    assert scheduleblock_3 is not None
    assert jsonable_encoder(scheduleblocks)
