import datetime

from database import Base
from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey


class Task(Base):
    __tablename__ = "task_db"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_db.id"))
    task_name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(Date, default=datetime.datetime.now().date())
    is_solved = Column(Boolean, default=False)
