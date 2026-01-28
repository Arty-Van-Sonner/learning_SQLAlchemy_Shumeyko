import datetime
from typing import Annotated
from turtle import update
from sqlalchemy import ForeignKey, Table, Column, Integer, String, MetaData, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text('TIMEZONE(\'utc\', now())'))]
updated_at = Annotated[
    datetime.datetime, 
    mapped_column(
        server_default=text('TIMEZONE(\'utc\', now())'), 
        onupdate=datetime.datetime.utcnow)
    ]

metadata_obj = Base.metadata

# Создание таблиц без использования полноценного ORM
employees_table = Table(
    'employees',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('username', String)
)

# ORM подход
class EmployeesOrm(Base):
    __tablename__ = 'employees_orm'
    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column()

    resumes: Mapped[list['ResumesOrm']] = relationship()

class Workload(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'

class ResumesOrm(Base):
    __tablename__ = 'resumes_orm'
    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[intpk]
    # title: Mapped[str] = mapped_column(String(128))
    title: Mapped[str_256]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees_orm.id', ondelete='CASCADE'))
    # created_at: Mapped[datetime.datetime] = mapped_column(server_default=text('TIMEZONE(\'utc\', now())'))
    # updated_at: Mapped[datetime.datetime] = mapped_column(
    #     server_default=text('TIMEZONE(\'utc\', now())'), 
    #     onupdate=datetime.utcnow)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    employee: Mapped['EmployeesOrm'] = relationship()
    
    repr_cols_num = 4
    repr_cols = ('create_at',)
