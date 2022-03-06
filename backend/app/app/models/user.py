from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .timetable import TimeTable  # noqa: F401
    from .color import Color  # noqa: F401


class User(Base):
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    kakao_id = Column(BigInteger, nullable=True)
    color_id = Column(Integer, ForeignKey("color.id"))
    nickname = Column(String, nullable=True)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    timetables = relationship("TimeTable", back_populates="owner")
    color = relationship("Color")
