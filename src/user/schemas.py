from pydantic import BaseModel, EmailStr, Field


class SRegistration(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr = Field(min_length=10)
    password: str = Field(min_length=8)
    repeat_password: str = Field(min_length=8)


class SLogin(BaseModel):
    email: EmailStr = Field(min_length=10)
    password: str = Field(min_length=8)
