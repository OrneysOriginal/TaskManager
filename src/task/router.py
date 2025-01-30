from datetime import datetime, timezone

import jwt
from fastapi import APIRouter, Depends, Request, HTTPException, status
from jose import JWTError
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY, ALGORITHM
from database import get_async_session
from task.schemas import STask, SDate
from task.models import Task
from user.models import User

task_router = APIRouter(
    prefix="/task",
    tags=["Task"],
)


def get_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_current_user(
    token: str = Depends(get_token), session: AsyncSession = Depends(get_async_session)
):
    try:
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token are not valid"
        )

    expire = token.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire is None or expire_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    user_id = token.get("user")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="ID not found"
        )

    query = select(User).filter(User.id == int(user_id))
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User are not found"
        )

    return user


@task_router.post("/add_task/")
async def add_task(
    data: STask,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> dict:
    query = select(Task).filter(Task.task_name == data.task_name)
    check_task = await session.execute(query)
    check_task = check_task.scalar_one_or_none()

    if check_task is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task with this name already created",
        )

    task = Task(user_id=user.id, task_name=data.task_name, description=data.description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return {"status_code": status.HTTP_200_OK}


@task_router.get("/get_all_task/")
async def get_all_task(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    query = select(Task).filter(Task.user_id == int(user.id))
    tasks = await session.execute(query)
    return {"status_code": status.HTTP_200_OK, "tasks": tasks.mappings().all()}


@task_router.post("/get_task_by_date/")
async def get_task_date(
    data: SDate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    query = select(Task).filter(
        (data.end_date > Task.created_at) & (Task.created_at > data.start_date)
    )
    tasks = await session.execute(query)
    return {"status_code": status.HTTP_200_OK, "tasks": tasks.mappings().all()}


@task_router.post("/del_task/")
async def del_task(
    task_name: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> dict:
    query = select(Task).filter(Task.task_name == task_name)
    check_task = await session.execute(query)
    check_task = check_task.scalar_one_or_none()
    if check_task is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task with this name are not created",
        )

    query = delete(Task).filter(Task.task_name == task_name)
    await session.execute(query)
    await session.commit()
    return {"status_code": status.HTTP_200_OK}
