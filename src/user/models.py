from database import Base
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(hash_password: str, planed_password: str) -> bool:
    return password_context.verify(hash_password, planed_password)
