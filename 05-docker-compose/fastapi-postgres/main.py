from typing import Union
from fastapi import FastAPI
import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

if (not dbname) or (not user) or (not password):
    raise ValueError("Database configuration environment variables are not set")

db_settings = f"dbname={dbname} user={user} password={password} host=database"

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = psycopg.connect(db_settings)
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
    item = cur.fetchone()
    cur.close()
    conn.close()
    print(item)
    if item:
        return {"id": item[0], "name": item[1], "description": item[2]}
    return {"error": "Item not found"}


@app.get("/db-test")
def db_test():
    conn = psycopg.connect(db_settings)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    cur.close()
    conn.close()
    return {"db_version": db_version}
