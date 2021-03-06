from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Color(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128))
    hex = Column(String(10))
