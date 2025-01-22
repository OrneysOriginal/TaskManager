from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, delete_tables
from user.router import user_router
from task.router import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(
    title="Отправить электронное письно",
    lifespan=lifespan,
)

app.include_router(
    user_router,
)

app.include_router(
    task_router,
)
