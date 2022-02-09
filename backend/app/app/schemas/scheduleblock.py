from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ScheduleBlockBase(BaseModel):
    table_id: str
    start_time: int
    start_minute: int
    end_time: int
    end_minute: int
    day: int
    label: Optional[str] = None


# 업데이트시 받을 데이터
class ScheduleBlockUpdate(ScheduleBlockBase):
    id: str


# 생성시 받을 데이터
class ScheduleBlockCreate(ScheduleBlockBase):
    pass


class ScheduleBlockInDBBase(ScheduleBlockBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "table_id": "450416ccb189c194b2c3bf4c7665725d",
                "start_time": 12,
                "start_minute": 0,
                "end_time": 15,
                "end_minute": 30,
                "day": 0,
                "lable": "학교 시험이 있어요",
            }
        }


# API 반환 데이터
class ScheduleBlock(ScheduleBlockInDBBase):
    pass


# DB에만 있는 데이터
class ScheduleBlockInDB(ScheduleBlockInDBBase):
    created_at: datetime
