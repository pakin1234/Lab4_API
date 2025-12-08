from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.db.models import Base
from app.core.settings import settings

DATABASE_URL = settings.database_url

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

@asynccontextmanager
async def get_transactional_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()  
        raise
    finally:
        await session.close()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_transactional_session() as session:
        yield session

async def init_models():
   async with async_engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)