from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager

from routers import users, section
from database import engine, get_db
import models


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend")

#routers
app.include_router(users.router, prefix="/user")
app.include_router(section.router, prefix="/section")


@app.get("/")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Question).options(
            selectinload(models.Question.author),
            selectinload(models.Question.replies).selectinload(models.Reply.author)
        )
    )
    questions = result.scalars().all()
    return templates.TemplateResponse(request, "index.html", {"posts": questions})