from pydantic import BaseModel, Field


class STask(BaseModel):
    task_name: str = Field(min_length=3)
    description: str = Field(min_length=3)
