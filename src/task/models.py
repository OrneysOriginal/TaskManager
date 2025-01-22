import datetime

from database import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey


def get_datetime_now():
    return datetime.datetime.now().date()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    task_name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_datetime_now)
    is_solved = Column(Boolean, default=False)
