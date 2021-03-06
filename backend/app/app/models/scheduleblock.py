from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .timetable import TimeTable  # noqa: F401
    from .user import User  # noqa: F401


class ScheduleBlock(Base):
    id = Column(String, primary_key=True, index=True)
    table_id = Column(String, ForeignKey("timetable.id"))
    user_id = Column(String, ForeignKey("user.id"))
    start_time = Column(SmallInteger)
    start_minute = Column(SmallInteger)
    end_time = Column(SmallInteger)
    end_minute = Column(SmallInteger)
    day = Column(SmallInteger)
    label = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    timetable = relationship("TimeTable", back_populates="scheduleblocks")
    user = relationship("User", backref="scheduleblocks")

    __table_args__ = (
        UniqueConstraint(
            "table_id",
            "user_id",
            "start_time",
            "start_minute",
            "end_time",
            "end_minute",
            "day",
            name="uc_time_table",
        ),
    )
