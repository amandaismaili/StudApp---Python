from __future__ import annotations
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    surname: Mapped[str] = mapped_column(String(25), nullable=False)
    university: Mapped[str] = mapped_column(String(35))
    degree: Mapped[str] = mapped_column(String(50))
    level: Mapped[str] = mapped_column(String(15))
    year: Mapped[int] = mapped_column(Integer)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

    posts: Mapped[list[Question]] = relationship(back_populates="author", cascade="all, delete-orphan")
    replies: Mapped[list[Reply]] = relationship(back_populates="author", cascade="all, delete-orphan")

    
class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    likes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    author: Mapped[User] = relationship(back_populates="posts")
    replies: Mapped[list[Reply]] = relationship(back_populates="question", cascade="all, delete-orphan")


class Reply(Base):
    __tablename__ = "replies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(UTC))
    likes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    
    author: Mapped[User] = relationship(back_populates="replies")
    question: Mapped[Question] = relationship(back_populates="replies")