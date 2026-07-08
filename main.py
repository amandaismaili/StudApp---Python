from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import users, section
from database import engine

@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI()

app.include_router(users.router, prefix="/user")
app.include_router(section.router, prefix="/section")