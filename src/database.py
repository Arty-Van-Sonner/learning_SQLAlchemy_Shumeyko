import asyncio
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, String, create_engine, text
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

class Base(DeclarativeBase):
    '''
    Docstring for Base
    '''
    type_annotation_map = {
        
    }
    def __repr__(self):
        cols = [f'{col}={getattr(self, col)}' for col  in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__} {", ".join(cols)}>'

sync_session = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine)

# with sync_engine.connect() as conn:
#     res = conn.execute(text('SELECT VERSION()'))
#     print(f'{res.all()=}')

# async def get_version():
#     async with async_engine.connect() as conn:
#         res = await conn.execute(text('SELECT VERSION()'))
#         print(f'{res.all()=}')

# asyncio.run(get_version())

str_256 = Annotated[str, 200]

class Base(DeclarativeBase):
    """
    Docstring for Base
    """
    repr_cols_num = 3
    repr_cols = tuple()

    type_annotation_map = {
        str_256: String(256)
    }
    def __repr__(self):
        # cols = [f'{col}={getattr(self, col)}' for col in self.__table__.columns.keys()]
        # return f'<{self.__class__.__name__} {", ".join(cols)}>'
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'