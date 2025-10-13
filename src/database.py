import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from src.queries.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycorg,
    echo=True, # Отображение запросов в базу в консоли
    pool_size=5, # Количество возможных подключений к базе
    max_overflow=10, # Количество дополнительных подключений к базе
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

# with sync_engine.connect() as conn:
#     res = conn.execute(text('SELECT VERSION()'))
#     print(f'{res.all()=}')

# async def get_version():
#     async with async_engine.connect() as conn:
#         res = await conn.execute(text('SELECT VERSION()'))
#         print(f'{res.all()=}')

# asyncio.run(get_version())