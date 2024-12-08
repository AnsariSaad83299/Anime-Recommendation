import pandas as pd
import streamlit as st
import psycopg2
from connector import get_db_connection
from admin_anime_data import create_anime, delete_anime, read_anime, update_anime
from admin_user_data import create_user, read_user, delete_user, update_user

def execute_query(query, conn, params=None):
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        conn.commit()

def get_table_columns(conn, table_name):
    query = """
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (table_name,))
        columns = cursor.fetchall()
    return columns  

st.sidebar.title("CRUD Operations")
page = st.sidebar.radio("Select a Page", ("User Profile Data", "Cleaned Anime Data"))

if page == "User Profile Data":
    action = st.selectbox("Select an action", ["Create", "Read", "Update", "Delete"])
    if action == "Create":
        create_user(get_db_connection())
    elif action == "Read":
        read_user(get_db_connection())
    elif action == "Update":
        update_user(get_db_connection())
    elif action == "Delete":
        delete_user(get_db_connection())

elif page == "Cleaned Anime Data":
    action = st.selectbox("Select an action", ["Create", "Read", "Update", "Delete"])
    if action == "Create":
        create_anime(get_db_connection())
    elif action == "Read":
        read_anime(get_db_connection())
    elif action == "Update":
        update_anime(get_db_connection())
    elif action == "Delete":
        delete_anime(get_db_connection())
