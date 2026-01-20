# from unittest import result
from sqlalchemy import text, insert, select
from src.database import sync_engine, async_session, sync_session
from src.models import metadata_obj, EmployeesOrm


class SyncOrm:
    """
    Docstring for SyncOrm
    """
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_employee():
        with sync_session() as session:
            employee_beaver = EmployeesOrm(username='Beaver')
            employee_wolf = EmployeesOrm(username='Wolf')
            session.add_all([employee_beaver, employee_wolf])
            session.flush()
            session.commit()

    @staticmethod
    def select_employee():
        with sync_session() as session:
            # employee_id = 1
            # employee_jack = session.get(EmployeesOrm, employee_id)
            query = select(EmployeesOrm)
            result = session.execute(query)
            employees = result.scalars().all()
            print(f'{employees=}')

    @staticmethod
    def update_employee(employee_id: int = 1, new_username: str = 'Kurl'):
        with sync_session() as session:
            employee_Jon = session.get(EmployeesOrm, employee_id)
            session.refresh()
            employee_Jon.username = new_username
            session.expire_all()
            session.commit()


class AsyncOrm:
    """
    Docstring for AsyncOrm
    """
    @staticmethod
    async def async_insert_data():
        async with async_session() as session:
            employee_beaver = EmployeesOrm(username='Beaver')
            employee_wolf = EmployeesOrm(username='Wolf')
            session.add_all([employee_beaver, employee_wolf])
            await session.commit()