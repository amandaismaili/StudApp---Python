from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

#schemas for users

#for sign up (public + private)
class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)
    name: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    university: str = Field(min_length=1)
    degree: str = Field(min_length=1)
    level: str = Field(min_length=1)
    year: int


class UserCreate(UserBase):
    password: str = Field(min_length=8)


#output schema(public + private)
class UserPublic(BaseModel):
    model_config =  ConfigDict(from_attributes=True)
    id: int
    username: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    university: str = Field(min_length=1)
    degree: str = Field(min_length=1)
    level: str = Field(min_length=1)
    year: int


class UserPrivate(UserPublic):
    email: EmailStr


class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = Field(default=None, min_length=1, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=20)
    surname: str | None = Field(default=None, min_length=1, max_length=25)
    university: str | None = Field(default=None, min_length=1, max_length=50)
    degree: str | None = Field(default=None, min_length=1, max_length=50)
    level: str | None = Field(default=None, min_length=1, max_length=50)
    year: int | None = Field(default=None)


#schemas for questions (considered posts)
class QuestionBase(UserBase):
    title: str = Field(min_length=10, max_length=100)
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    date_posted: datetime
    author: UserPublic


class QuestionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    text: str | None = Field(default=None, min_length=1)


#schemas for replies
class ReplyCreate(BaseModel):
    text: str = Field(default= None, min_length=1)


class ReplyResponse(BaseModel):
    text: str = Field(default=None, min_length=1)
    id: int
    user_id: int
    post_id: int
    date_published: datetime
    author: UserPublic


class ReplyUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1)


#schema for login
class Token(BaseModel):
    access_token: str
    token_type: str 