from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .scheduleblock import ScheduleBlock  # noqa: F401
    from .user import User  # noqa: F401


class TimeTable(Base):
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    create_user_id = Column(String, ForeignKey("user.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="timetables")
    scheduleblocks = relationship("ScheduleBlock", back_populates="timetable")
