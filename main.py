from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from routers import users, section
from database import engine



@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

#routers
app.include_router(users.router, prefix="/user")
app.include_router(section.router, prefix="/section")