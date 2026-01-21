# from unittest import result
from turtle import title
from sqlalchemy import Integer, text, insert, select, func, cast, and_
from src.database import sync_engine, async_session, sync_session
from src.models import metadata_obj, EmployeesOrm, ResumesOrm, Workload


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

            employee_Andziej = EmployeesOrm(username='Andziej')
            employee_Jon = EmployeesOrm(username='Jon')

            session.add_all([employee_beaver, employee_wolf, employee_Andziej, employee_Jon])
            session.flush()
            session.commit()

    @staticmethod
    def insert_resumes():
        with sync_session() as session:
            # query = select(EmployeesOrm)
            # result = session.execute(query)
            # employees = result.scalars().all()
            # employees_dict = {}
            # for employee in employees:
            #     employees_dict[employee.id] = employee
            resumes = [
                ResumesOrm(
                    title='Python Junior Developer',
                    compensation=50000,
                    workload=Workload.fulltime,
                    employee_id=1,
                ),
                ResumesOrm(
                    title='Python Developer',
                    compensation=150000,
                    workload=Workload.fulltime,
                    employee_id=1,
                ),
                ResumesOrm(
                    title='Python Data Engineer',
                    compensation=250000,
                    workload=Workload.parttime,
                    employee_id=2,
                ),
                ResumesOrm(
                    title='Data Scientist',
                    compensation=300000,
                    workload=Workload.fulltime,
                    employee_id=2,
                ),
            ]
            session.add_all(resumes)
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
    def select_resumes_avg_compensation(like_language: str = 'Python'):
        """
        Docstring for select_resumes_avg_compensation

        select
            workload, 
            avg(compensation) as avg_compensation
        from 
            resumes_orm
        where 
            title like '%Python%'
            and compensation > 40000
        group by
            workload
        """
        with sync_session() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label('avg_compensation'),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000) 
            )
            print(f'\n\n{query}\n\n')
            print(f'\n\n{query.compile(compile_kwargs={"literal_binds": True})}\n\n')
            res = session.execute(query)
            result = res.all()
            print(f'\n\n{result}\n\n')
            print(f'\n\n{result[0].avg_compensation}\n\n')

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