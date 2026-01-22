# from unittest import result
from turtle import title
from unittest import result
from sqlalchemy import Integer, text, insert, select, func, cast, and_
from sqlalchemy.orm import aliased
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

    @staticmethod
    def insert_additional_resumes():
        with sync_session() as session:
            employees = {employee: EmployeesOrm(username=employee) for employee in ['Artem', 'Roman', 'Petr']}
            session.add_all(employees.values())
            session.flush()
            resumes = [
                {'title': 'Python Developer', 'compensation': 60000, 'workload': Workload.fulltime, 'employee_id': employees['Artem'].id},
                {'title': 'Machin Learning Engineer', 'compensation': 70000, 'workload': Workload.parttime, 'employee_id': employees['Artem'].id},
                {'title': 'Python Data Scientist', 'compensation': 80000, 'workload': Workload.parttime, 'employee_id': employees['Roman'].id},
                {'title': 'Python Analyst', 'compensation': 90000, 'workload': Workload.fulltime, 'employee_id': employees['Roman'].id},
                {'title': 'Python Junior Developer', 'compensation': 100000, 'workload': Workload.fulltime, 'employee_id': employees['Petr'].id},
            ]
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_resumes)
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

    @staticmethod
    async def join_cte_subquery_window_func(like_language: str = 'Python'):
        """
        with helper2 as (
            select 
                *,
                compensation-avg_employee_compensation as compensation_diff
            from
                (select
                    e.id as id,
                    e.username as username,
                    r.compensation as compensation,
                    r.workload as workload,
                    avg(r.compensation) over (partition by r.workload)::int as avg_employee_compensation
                from 
                    resumes_orm as r
                    join employees_orm as e
                        on r.employee_id = e.id) as helper1
        )
        select 
            *
        from 
            helper2
        order by 
            compensation_diff desc
        """
        async with async_session() as session:
            r = aliased(ResumesOrm)
            w = aliased(EmployeesOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label('avg_employee_compensation')
                )
                # .select_from(r)
                # .join(full=True, or isouter=True : (left join))
                .join(r, r.employee_id == w.id).subquery('helper1')
            )
            cte = (
                select(
                    subq.c.employee_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_employee_compensation,
                    (subq.c.compensation - subq.c.avg_employee_compensation).label('compensation_diff') # compensation-avg_employee_compensation as compensation_diff
                )
                .cte('helper2')
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            # print(query.compile(compile_kwargs={'literal_binds': True}))

            res = await session.execute(query)
            result = res.all()

            print(f'\n\n{result=}\n\n')