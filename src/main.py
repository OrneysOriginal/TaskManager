from fastapi import FastAPI
from user.router import user_router
from task.router import task_router


app = FastAPI(
    title="Отправить электронное письно",
)

app.include_router(
    user_router,
)

app.include_router(
    task_router,
)
