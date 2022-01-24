from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

# 개발할 때 여기서 모든 API 만들고 나중에 모듈화 진행할 예정임

@router.get("/")
def root():
    return "hello world!"


@router.get("/timetable/{timetable_id}", response_model=schemas.TimeTable, response_model_exclude_unset=True)
def get_timetable_by_id(
    timetable_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    TODO: 스케쥴 블록 어떻게 전달할지 결정해야 함
    """
    timetables = crud.timetable.get(db, id=timetable_id)
    return timetables


@router.post("/timetable", response_model=schemas.TimeTable, response_model_exclude=True)
def create_timetable(
    *,
    db: Session = Depends(deps.get_db),
    timetable_in: schemas.TimeTableCreate
):
    timetable = crud.timetable.create(db, obj_in=timetable_in)
    return timetable


@router.put("/timetable")
def update_timetable_by_id(
    *,
    timetable_id: str,
    db: Session = Depends(deps.get_db),
    timetable_in: schemas.TimeTableUpdate
):
    """시간표 정보 수정

    Args:
        timetable_id (str): [description]
        timetable_in (schemas.TimeTableUpdate): [description]
        db (Session, optional): [description]. Defaults to Depends(deps.get_db).

    Returns:
        [type]: [description]
    """
    timetable = crud.timetable.update(db, obj_in=timetable_in)
    return timetable



@router.post("/scheduleblock")
def create_scheduleblock(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblock_in: schemas.ScheduleBlockCreate
):
    """
    스케쥴 블록 생성 로직 Array로 받아서 한번에 넣어줘야 하나 고민...
    일단 하나만 생성하는 것 만들기로 함
    """
    scheduleblock = crud.scheduleblock.create(db, obj_in=scheduleblock_in)
    return scheduleblock