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


@router.get("/search/{question_id}", response_model=QuestionResponse)
async def search(question_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Question).where(models.Question.id == question_id).options(selectinload(models.Question.author)))
    question = result.scalars().first()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Question not found")
    
    return question


@router.delete("/delete/question/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, current_user: currentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    res = await db.execute(select(models.Question).where(models.Question.id == question_id))
    result = res.scalars().first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Question not found.")
    
    if result.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Cannot delete this question.")
    
    await db.delete(result)
    await db.commit()

    return None


@router.delete("/delete/reply/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reply(reply_id: int, current_user: currentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    res = await db.execute(select(models.Reply).where(models.Reply.id == reply_id))
    result = res.scalars().first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Reply not found.")
    
    if result.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Cannot delete this reply.")
    
    await db.delete(result)
    await db.commit()

    return None


@router.patch("/update/{question_id}", response_model=QuestionResponse)
async def update_question(question_id: int, current_user: currentUser, ques_data: QuestionUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    res = await db.execute(select(models.Question).where(models.Question.id == question_id).options(selectinload(models.Question.author)))
    result = res.scalars().first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Question not found.")
    
    if result.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Cannot edit this question.")
    
    update_data = ques_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(result, field, value)

    await db.commit()
    await db.refresh(result, attribute_names=["author"])

    return result


@router.patch("/update/{reply_id}", response_model=ReplyResponse)
async def update_reply(reply_id: int, current_user: currentUser, reply_data: ReplyUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    res = await db.execute(select(models.Reply).where(models.Reply.id == reply_id).options(selectinload(models.Reply.author)))
    result = res.scalars().first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Reply not found.")
    
    if result.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Cannot edit this reply.")
    
    update_data = reply_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(result, field, value)

    await db.commit()
    await db.refresh(result, attribute_names=["author"])

    return result