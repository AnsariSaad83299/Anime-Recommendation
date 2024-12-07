import pandas as pd
from sqlalchemy import create_engine
import psycopg2

db_connection = "postgresql://postgres:password@localhost:5432/anime-recommendation"
sqlalchecmy_engine = create_engine(db_connection)

def get_db_connection():
    return psycopg2.connect(
    dbname="anime-recommendation",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
    )