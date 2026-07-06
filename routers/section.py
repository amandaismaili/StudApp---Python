from fastapi import HTTPException, APIRouter, Depends, status
from typing import Annotated

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from schemas import QuestionCreate, QuestionResponse, QuestionUpdate, ReplyCreate, ReplyResponse, ReplyUpdate
from database import get_db
from authenticate import currentUser

router = APIRouter()


@router.get("", response_model=list[QuestionResponse])
async def get_section(db: Annotated[AsyncSession, Depends(get_db)]):
    res = await db.execute(select(models.Question).options(selectinload(models.Question.author), selectinload(models.Question.replies)))
    data = res.scalars().all()
    return data


@router.post("/questions", response_model= QuestionResponse, status_code=status.HTTP_201_CREATED)
async def make_question(ques: QuestionCreate, current_user: currentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    question = models.Question(
        user_id = current_user.id,
        title = ques.title,
        text = ques.text
    )

    db.add(question)
    await db.commit()
    await db.refresh(question, attribute_names=["author"])
    return question


@router.post("/{question_id}/reply", response_model= ReplyResponse, status_code= status.HTTP_201_CREATED)
async def reply_to_ques(question_id: int, reply_body: ReplyCreate, current_user: currentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    reply = models.Reply(
        user_id = current_user.id,
        text = reply_body.text,
        question_id = question_id
    )

    db.add(reply)
    await db.commit()
    await db.refresh(reply, attribute_names=["author"])
    return reply

