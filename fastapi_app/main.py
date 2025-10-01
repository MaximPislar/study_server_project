from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi_app.database import db_helper
from fastapi_app.routers import router as user_router
from fastapi_app.routers.home import router as home_router  # Todo add router to __init__


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(home_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
