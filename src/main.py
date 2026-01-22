import asyncio
import os
import sys

from fastapi import FastAPI
import uvicorn

sys.path.insert(1, os.path.join(sys.path[0], '..'))

# from src.queries.core import create_tables, drop_tables, insert_data_query_builder, insert_data_sql_request
from src.queries.core import SyncCore, AsyncCore
# from src.queries.orm import async_insert_data, create_tables as create_tables_orm, insert_data
from src.queries.orm import SyncOrm, AsyncOrm

# SyncCore.drop_tables()
# SyncCore.create_tables()
# SyncCore.insert_data_query_builder()

# create_tables_orm()
# insert_data()
# asyncio.run(async_insert_data())

# SyncCore.update_employee()

# SyncCore.update_employee_orm()

# SyncCore.select_employees()

# SyncOrm.insert_employee()

# SyncOrm.select_employee()
# print()
# SyncOrm.update_employee()
# print()
# SyncOrm.select_employee()

# SyncOrm.insert_resumes()

# SyncOrm.select_resumes_avg_compensation()

# SyncOrm.insert_additional_resumes()

# asyncio.run(AsyncOrm.join_cte_subquery_window_func())

async def main():
    # ========== SYNC ==========
    #CORE
    if '--core' in sys.argv and '--sync' in sys.argv:
        if '--create' in sys.argv:
            SyncCore.create_tables()
        if '--get' in sys.argv:
            SyncCore.select_employees()
            SyncCore.select_resumes_avg_compensation()
            SyncCore.join_cte_subquery_window_func()


    # ========== ASYNC ==========
    # if 

    await AsyncOrm.join_cte_subquery_window_func()

if __name__ == '__main__':
    asyncio.run(main())
    if "--webserver" in sys.argv:
        uvicorn.run(
            app="src.main:app",
            reload=True,
        )
