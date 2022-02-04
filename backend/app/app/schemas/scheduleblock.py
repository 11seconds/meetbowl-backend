from datetime import datetime, time
from pydoc import describe
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ScheduleBlockBase(BaseModel):
    table_id: str
    start_time: time
    end_time: Optional[time] = None
    day: Optional[int]
    label: Optional[str] = None
    


#업데이트시 받을 데이터
class ScheduleBlockUpdate(ScheduleBlockBase):
    id: str


# 생성시 받을 데이터
class ScheduleBlockCreate(ScheduleBlockBase):
    start_time: time
    end_time: Optional[time]
    
    
class ScheduleBlockInDBBase(ScheduleBlockBase):
    id: str
    created_at: datetime
    user_id: str
    class config:
        orm_mode=True
        

# API 반환 데이터
class ScheduleBlock(ScheduleBlockInDBBase):
    pass


# DB에만 있는 데이터
class ScheduleBlockInDB(ScheduleBlockInDBBase):
    pass
