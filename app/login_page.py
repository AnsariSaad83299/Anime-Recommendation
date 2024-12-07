import streamlit as st
import psycopg2
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = psycopg2.connect(
        dbname="anime-recommendation",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    hashed_password = hash_password(password)
    cur.execute('''
        SELECT * FROM users
        WHERE username = %s AND password = %s
    ''', (username, hashed_password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

st.title("Login")
username = st.text_input("Enter Username")
password = st.text_input("Enter Password", type="password")
if st.button("Login"):
    user = authenticate_user(username, password)
    if user:
        st.session_state["username"] = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password.")

