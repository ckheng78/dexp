from .db import dexp_db
from fastapi import FastAPI

app = FastAPI()
db = dexp_db()

@app.get("/show_tables")
async def show_tables():
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    result = db.execute_query(query)
    return {"tables": [row[0] for row in result]}

@app.get("/show_columns/{table_name}")
async def show_columns(table_name: str):
    query = f"PRAGMA table_info({table_name})"
    result = db.execute_query(query)
    return {"columns": [row[1] for row in result]}

