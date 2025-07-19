from .db import dexp_db
from fastapi import FastAPI

app = FastAPI()
db = dexp_db()

def _get_table_names():
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    result = db.execute_query(query)
    return [row[0] for row in result]

@app.get("/get_table_names")
async def get_table_names():
    return {"tables": _get_table_names()}

def _get_columns(table_name: str):
    query = f"PRAGMA table_info({table_name})"
    result = db.execute_query(query)
    return [row[1] for row in result]  # Return column names

@app.get("/get_columns/{table_name}")
async def get_columns(table_name: str):
    return {"columns": _get_columns(table_name)}

def _get_data(table_name: str, row_limit: int):
    query = f"SELECT * FROM {table_name} LIMIT {row_limit}"
    result = db.execute_query(query)
    return [dict(zip([column for column in _get_columns(table_name)], row)) for row in result]

@app.get("/get_data/{table_name}")
async def get_data(table_name: str, row_limit: int = 10):
    return {"data": _get_data(table_name, row_limit)}

def _get_schema():
    schema = {}
    for table in _get_table_names():
        schema[table] = _get_columns(table)
    return schema

@app.get("/get_schema")
async def get_schema():
    return {"schema": _get_schema()}