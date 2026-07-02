from fastapi import HTTPException, status, Depends
from typing import Annotated
import models
from schemas import UserBase, UserCreate, UserPrivate, UserPublic, UserUpdate, Token

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

#dont forget from login file and config

