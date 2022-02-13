from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models import scheduleblock

router = APIRouter()


@router.post("/scheduleblocks", status_code=201, response_model=schemas.ScheduleBlock)
def create_scheduleblock(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblock_in: schemas.ScheduleBlockCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    스케쥴 블록 생성 API
    """
    scheduleblock = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in, user_id=current_user.id
    )

    return scheduleblock


@router.patch("/scheduleblocks", status_code=201)
def update_scheduleblock_by_id(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblocks_in: List[schemas.ScheduleBlockUpdate],
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """ 스케쥴 블록 수정
    JWT 필요
    """

    scheduleblocks: List[scheduleblock.ScheduleBlock] = []

    for scheduleblock_in in scheduleblocks_in:
        scheduleblock_db = crud.scheduleblock.get(db, id=scheduleblock_in.id)

        if scheduleblock_db is None:
            raise HTTPException(status_code=404, detail="Scheduleblock not found")

        if scheduleblock_db.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges"
            )

        updated_scheduleblock = crud.scheduleblock.update(
            db, db_obj=scheduleblock_db, obj_in=scheduleblock_in
        )

        scheduleblocks.append(updated_scheduleblock)
    return scheduleblocks


@router.delete("/scheduleblocks/{scheduleblock_id}")
def delete_scheduleblock_by_id(
    scheduleblock_id: str,
    db: Session = Depends(deps.get_db),
    *,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    scheduleblock_db = crud.scheduleblock.get(db, id=scheduleblock_id)

    if scheduleblock_db is None:
        raise HTTPException(status_code=404, detail="Scheduleblock not found")

    if scheduleblock_db.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )

    _return = crud.scheduleblock.remove(db, id=scheduleblock_db.id)

    return _return
