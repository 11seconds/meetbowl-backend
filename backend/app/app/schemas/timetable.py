from pydoc import describe
from typing import Optional

from pydantic import BaseModel


# Shared properties
class TimeTableBase(BaseModel):
    title: str
    description: Optional[str] = None
    create_user_id: str


#업데이트시 받을 데이터
class TimeTableUpdate(TimeTableBase):
    id: str
    create_user_id: str
    title: str
    description: Optional[str]


# 생성시 받을 데이터
class TimeTableCreate(TimeTableBase):
    title: str
    description: Optional[str]
    create_user_id: str
    

# API 반환 데이터
class TimeTable(TimeTableBase):
    id: str
    class Config:
        orm_mode = True
