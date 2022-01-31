from datetime import datetime
from pydoc import describe
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ScheduleBlockBase(BaseModel):
    id: str
    table_id: str
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    label: Optional[str] = None


#업데이트시 받을 데이터
class ScheduleBlockUpdate(ScheduleBlockBase):
    user_id: str


# 생성시 받을 데이터
class ScheduleBlockCreate(ScheduleBlockBase):
    user_id: str
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    label: Optional[str]
    
    
class ScheduleBlockInDBBase(ScheduleBlockBase):
    created_at: datetime
    class config:
        orm_mode=True
        

# API 반환 데이터
class ScheduleBlock(ScheduleBlockInDBBase):
    pass


# DB에만 있는 데이터
class ScheduleBlockInDB(ScheduleBlockInDBBase):
    pass
