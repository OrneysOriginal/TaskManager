from pydantic import BaseModel, Field
from datetime import date


class STask(BaseModel):
    task_name: str = Field(min_length=3)
    description: str = Field(min_length=3)


class SDate(BaseModel):
    start_date: date = Field()
    end_date: date = Field()
