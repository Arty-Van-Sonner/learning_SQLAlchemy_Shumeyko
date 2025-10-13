from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_obj = MetaData()

employees_table = Table(
    'employees',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('username', String)
)
