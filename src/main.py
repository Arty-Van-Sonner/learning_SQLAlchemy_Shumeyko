import asyncio
import os
import sys

from fastapi import FastAPI

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.queries.core import create_tables, drop_tables, insert_data_query_builder, insert_data_sql_request

# drop_tables()
# create_tables()
insert_data_query_builder()
