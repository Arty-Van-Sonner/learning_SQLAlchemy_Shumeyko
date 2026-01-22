# from turtle import update
from sqlalchemy import insert, text, select, update
from src.database import sync_engine, async_engine, sync_session
from src.models import employees_table, metadata_obj


class SyncCore:
    @staticmethod
    def drop_tables():
        metadata_obj.drop_all(sync_engine)

    @staticmethod
    def create_tables():
        metadata_obj.create_all(sync_engine)

    @staticmethod
    def insert_data_sql_request():
        with sync_engine.connect() as conn:
            stmt = """INSERT INTO employees (username) VALUES
            ('AO Bobr'),
            ('OOO Volk');"""
            conn.execute(text(stmt))
            conn.commit()

    @staticmethod
    def insert_data_query_builder():
        with sync_engine.connect() as conn:
            stmt = insert(employees_table).values(
                [
                    {'username': 'Beaver',},
                    {'username': 'Wolf',},
                    {'username': 'Andziej',},
                    {'username': 'Jon',},
                ]
            )
            conn.execute(stmt)
            conn.commit() 

    @staticmethod
    def select_employees():
        with sync_engine.connect() as conn:
            query = select(employees_table)
            result = conn.execute(query)
            employees = result.all()
            print(f'{employees=}')

    @staticmethod
    def update_employee(employee_id: int = 2, new_username: str = 'Michael'):
        with sync_engine.connect() as conn:
            stmt = text('UPDATE employees_orm SET username=:new_username WHERE id=:employee_id')
            stmt = stmt.bindparams(new_username=new_username, employee_id=employee_id)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def update_employee_orm(employee_id: int = 4, new_username: str = 'Filip', **filter_by):
        with sync_engine.connect() as conn:
            # stmt = (
            #     update(employees_table)
            #     .values(username=new_username)
            #     .where(employees_table.c.id==employee_id)
            # )
            stmt = (
                update(employees_table)
                .values(username=new_username)
                .filter_by(id=employee_id)
            )
            conn.execute(stmt)
            conn.commit()

class AsyncCore:
    """
    Docstring for AsyncCore
    """
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.create_all)

    @staticmethod
    async def drop_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)