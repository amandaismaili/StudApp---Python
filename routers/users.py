from fastapi import HTTPException, status, Depends, APIRouter
from typing import Annotated
import models
from schemas import UserBase, UserCreate, UserPrivate, UserPublic, UserUpdate, Token

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from authenticate import currentUser, create_token, hash_pw, verify_pw
from config import settings
from database import get_db


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db:Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.username) == user.username)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Username already exists."
        )
    
    result = await db.execute(select(models.User).where(models.User.email) == user.email)
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Email already exists."
        )
    
    new_user = models.User(
        username = user.username,
        email = user.email,
        name = user.name,
        surname = user.surname,
        university = user.university,
        degree = user.degree,
        level = user.level,
        year = user.year,
        password_hash = hash_pw(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh()
    return new_user


@router.post("/login", response_model=Token)
async def login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):
    res = await db.execute(select(models.User).where(
        or_(
            (models.User.email) == form_data.username,
            models.User.username == form_data.username
            )
       )
    )

    user = res.scalars().first()
    if not user or not verify_pw(form_data.pw, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes = settings.access_token_expire_minutes)
    access_token = create_token(
        data = {"sub": str(user.id)},
        expires_delta = access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPrivate)
async def get_current_user(current_user: currentUser):
    return current_user
