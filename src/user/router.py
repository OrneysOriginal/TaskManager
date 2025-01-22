from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from user.auth import create_access_token
from user.models import hashed_password, User, verify_password
from user.schemas import SRegistration, SLogin
import secrets


user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post("/registration/")
async def register_post(
    data: SRegistration = Depends(), session: AsyncSession = Depends(get_async_session)
) -> dict:
    if not secrets.compare_digest(data.password, data.repeat_password):
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Password and repeatable password dont match",
        )

    query = select(User).filter(
        User.email == data.email or User.username == data.username
    )
    required_user = await session.execute(query)
    required_user = required_user.scalar_one_or_none()
    if required_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already registered",
        )

    hashed_pwd = hashed_password(data.password)
    user = User(username=data.username, email=data.email, hash_password=hashed_pwd)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"user": user}


@user_router.post("/login/")
async def login(
    response: Response,
    data: SLogin = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    user = await authenticate(data, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or email",
        )

    access_token = await create_access_token({"user": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    return {"access_token": access_token}


async def authenticate(
    data: SLogin = Depends(), session: AsyncSession = Depends(get_async_session)
) -> User:
    query = select(User).filter(User.email == data.email)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email - not found",
        )

    if verify_password(user.hash_password, hashed_password(data.password)):
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Incorrect password"
        )

    return user
