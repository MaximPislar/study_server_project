from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_helper.dispose()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app")
