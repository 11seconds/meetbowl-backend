from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class TimeTableBase(BaseModel):
    title: Optional[str]
    description: Optional[str] = None


# 업데이트시 받을 데이터
class TimeTableUpdate(TimeTableBase):
    title: str
    description: Optional[str]


# 생성시 받을 데이터
class TimeTableCreate(TimeTableBase):
    title: str
    description: Optional[str]


class TimeTableInDBBase(TimeTableBase):
    id: str
    create_user_id: str

    class Config:
        orm_mode = True


# API 반환 데이터
class TimeTable(TimeTableInDBBase):
    pass


class TimeTableInDB(TimeTableInDBBase):
    created_at: datetime
