import asyncio
import os
import sys

from fastapi import FastAPI

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.queries.core import create_tables, drop_tables, insert_data_query_builder, insert_data_sql_request
from src.queries.orm import async_insert_data, create_tables as create_tables_orm, insert_data

# drop_tables()
# create_tables()
# insert_data_query_builder()
create_tables_orm()
# insert_data()
# asyncio.run(async_insert_data())
