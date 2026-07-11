from fastapi import HTTPException, status, Depends, APIRouter
from typing import Annotated
import models
from schemas import UserBase, UserCreate, UserPrivate, UserPublic, UserUpdate, Token

from sqlalchemy import select, or_
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
    result = await db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Username already exists."
        )
    
    result = await db.execute(select(models.User).where(models.User.email == user.email))
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
    await db.refresh(new_user)
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
    if not user or not verify_pw(form_data.password, user.password_hash):
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


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_acc(user_id: int, current_user: currentUser, db:Annotated[AsyncSession, Depends(get_db)]):
    if user_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to delete this account."
        )
    
    result = await db.execute(select(models.User).where(models.User.id == user_id).options(selectinload(models.User.posts)))
    currUser = result.scalars().first()
    if not currUser:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    await db.delete(currUser)
    await db.commit()
    return None


@router.put("/search/{user_id}", response_model=UserPrivate)
async def update_account(user_id: int, current_user: currentUser, user_update: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    if user_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to update this account."
        )
    
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    result = res.scalars().first()

    if not result:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )
    
    if user_update.username is not None and user_update.username != result.username:
        res = await db.execute(select(models.User).where(models.User.username == user_update.username))
        existing_user = res.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail = "Username already exists."
            )
        

    if user_update.email is not None and user_update.email != result.email:
        res = await db.execute(select(models.User).where(models.User.email == user_update.email))
        existing_email = res.scalars().first()

        if existing_email:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail = "Email has already been used."
            )
        
    if user_update.username is not None:
        result.username = user_update.username
    if user_update.email is not None:
        result.email = user_update.email
    if user_update.name is not None:
        result.name = user_update.name
    if user_update.surname is not None:
        result.surname = user_update.surname
    if user_update.university is not None:
        result.university = user_update.university
    if user_update.degree is not None:
        result.degree = user_update.degree
    if user_update.year is not None:
        result.year = user_update.year
    if user_update.level is not None:
        result.level = user_update.level

    await db.commit()
    await db.refresh(result)
    
    return result