from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
#from config import settings - add the ones with settings in it

class Base(DeclarativeBase):
    pass