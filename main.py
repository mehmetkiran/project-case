from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import user, chat, pdf
from db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(chat.router)
app.include_router(pdf.router)
