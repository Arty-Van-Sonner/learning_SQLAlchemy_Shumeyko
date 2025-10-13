from sqlalchemy import insert, text
from src.database import sync_engine, async_engine
from src.models import employees_table, metadata_obj

def drop_tables():
    metadata_obj.drop_all(sync_engine)

def create_tables():
    metadata_obj.create_all(sync_engine)

def insert_data_sql_request():
    with sync_engine.connect() as conn:
        stmt = """INSERT INTO employees (username) VALUES
        ('AO Bobr'),
        ('OOO Volk');"""
        conn.execute(text(stmt))
        conn.commit()

def insert_data_query_builder():
    with sync_engine.connect() as conn:
        stmt = insert(employees_table).values(
            [
                {'username': 'Beaver',},
                {'username': 'Wolf',},
            ]
        )
        conn.execute(stmt)
        conn.commit() 