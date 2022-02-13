from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/timetables/{timetable_id}", response_model=schemas.TimeTable)
def get_timetable_by_id(timetable_id: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    타임테이블 정보 보기
    """
    timetables = crud.timetable.get(db, id=timetable_id)
    if timetables is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetables


@router.get(
    "/timetables/{timetable_id}/scheduleblocks",
    response_model=List[schemas.ScheduleBlock],
)
def get_scheduleblocks_by_timetable_id(
    timetable_id: str, db: Session = Depends(deps.get_db)
) -> Any:
    """
    타임테이블의 스케쥴 블록 조회
    """
    scheduleblock = crud.scheduleblock.get_all(db, table_id=timetable_id)
    return scheduleblock


@router.get(
    "/timetables/{timetable_id}/scheduleblocks/me",
    response_model=List[schemas.ScheduleBlock],
)
def get_my_scheduleblocks_by_timetable_id(
    timetable_id: str,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    로그인한 유저 본인의 타임테이블의 스케쥴 블록 조회
    """
    scheduleblocks = crud.scheduleblock.get_all_by_user_id(
        db, table_id=timetable_id, user_id=current_user.id
    )
    return scheduleblocks


@router.post("/timetables", response_model=schemas.TimeTable, status_code=201)
def create_timetable(
    *,
    db: Session = Depends(deps.get_db),
    timetable_in: schemas.TimeTableCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    타임테이블 생성
    """
    timetable = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=current_user.id
    )
    if not timetable:
        raise HTTPException(status_code=500, detail="Timetable is not created")
    return timetable


@router.patch(
    "/timetables/{timetable_id}", response_model=schemas.TimeTable, status_code=201
)
def update_timetable_by_id(
    *,
    db: Session = Depends(deps.get_db),
    timetable_id: str,
    timetable_in: schemas.TimeTableUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    시간표 정보 수정
    JWT 필요
    """
    timetable_db = crud.timetable.get(db, timetable_id)

    if timetable_db is None:
        raise HTTPException(status_code=404, detail="Timetable not found")

    if timetable_db.create_user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges. Only timetable owner can update info.",
        )

    return_timetable = crud.timetable.update(
        db, db_obj=timetable_db, obj_in=timetable_in
    )
    return return_timetable
