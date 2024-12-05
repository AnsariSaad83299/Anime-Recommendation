import streamlit as st
import psycopg2
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def add_user_to_db(username, password):
    conn = psycopg2.connect(
        dbname="anime-recommendation",
        user="postgres",
        password="pgsql",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cur.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        ''', (username, hashed_password))
        conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

st.title("Signup")
username = st.text_input("Enter Username")
password = st.text_input("Enter Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
if st.button("Sign Up"):
    if password != confirm_password:
        st.error("Passwords do not match.")
    else:
        success = add_user_to_db(username, password)
        if success:
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists. Please try another one.")
