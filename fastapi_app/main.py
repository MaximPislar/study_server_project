from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi_app.database import db_helper
from fastapi_app.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
