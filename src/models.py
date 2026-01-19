from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

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
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
