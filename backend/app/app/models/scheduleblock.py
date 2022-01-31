from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .scheduleblock import ScheduleBlock  # noqa: F401


class ScheduleBlock(Base):
    id = Column(String, primary_key=True, index=True)
    table_id = Column(String, ForeignKey("timetable.id"))
    user_id = Column(String, ForeignKey("user.id"))
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    label = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    timetable = relationship("TimeTable", back_populates="scheduleblocks")