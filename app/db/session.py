from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

db_url = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"
# print(f"DEBUG --  подключаемся к базе: {db_url}")

engine = create_async_engine(db_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
