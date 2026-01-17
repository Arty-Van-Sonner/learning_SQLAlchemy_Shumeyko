from sqlalchemy import text, insert
from src.database import sync_engine, async_session, sync_session
from src.models import metadata_obj, EmployeesOrm

def create_tables():
    sync_engine.echo = False
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True

def insert_data():
    with sync_session() as session:
        employee_beaver = EmployeesOrm(username='Beaver')
        employee_wolf = EmployeesOrm(username='Wolf')
        session.add_all([employee_beaver, employee_wolf])
        session.commit()

async def async_insert_data():
    async with async_session() as session:
        employee_beaver = EmployeesOrm(username='Beaver')
        employee_wolf = EmployeesOrm(username='Wolf')
        session.add_all([employee_beaver, employee_wolf])
        await session.commit()