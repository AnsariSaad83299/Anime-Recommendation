import pandas as pd
import streamlit as st

def get_ids(conn):
    query = f"SELECT username FROM user_profile_data"
    with conn.cursor() as cursor:
        cursor.execute(query)
        ids = [row[0] for row in cursor.fetchall()]
    return ids

def get_row_by_id(conn, username):
    query = "SELECT * FROM user_profile_data WHERE username = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]
    return dict(zip(column_names, row)) if row else None

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

def create_user(conn):
    st.header("Create User Profile")

    columns = get_table_columns(conn, "user_profile_data")
    
    user_data = {}
    for col_name, data_type in columns:
        if col_name.lower() == "user_id" or col_name.lower() == "user_id":
            continue
        if "date" in data_type:
            user_data[col_name] = st.date_input(f"Enter {col_name}")
        elif "int" in data_type:
            user_data[col_name] = st.number_input(f"Enter {col_name}", step=1)
        else:
            user_data[col_name] = st.text_input(f"Enter {col_name}")

    if st.button("Create User"):
        column_names = ", ".join(user_data.keys())
        placeholders = ", ".join(["%s"] * len(user_data))
        query = f"INSERT INTO user_profile_data ({column_names}) VALUES ({placeholders})"
        
        execute_query(query, conn, tuple(user_data.values()))
        st.success("User created successfully!")

def read_user(conn):
    st.header("Read User Profile Data")
    
    query = "SELECT * FROM user_profile_data LIMIT 10"
    df = pd.read_sql(query, conn)
    st.write(df)

    st.header("Get Particular User Profile Data")
    usernames = get_ids(conn)
    selected_username = st.selectbox("Select User ID", usernames, key="select_user_read")

    if selected_username:
        user_details = get_row_by_id(conn, selected_username)
        if user_details:
            st.subheader("User Details")
            st.table(user_details)
        else:
            st.warning("User not found.")

def delete_user(conn):
    st.header("Delete User Profile")
    
    usernames = get_ids(conn)
    selected_username = st.selectbox("Select User ID to Delete", usernames)
    
    if st.button("Delete User"):
        query = "DELETE FROM user_profile_data WHERE username = %s"
        execute_query(query, conn, (selected_username,))
        st.success("User deleted successfully!")

def update_user(conn):
    st.header("Update User Profile")

    usernames = get_ids(conn)
    selected_username = st.selectbox("Select User ID to Update", usernames)
    
    columns = get_table_columns(conn, "user_profile_data")

    user_data = {}
    for col_name, data_type in columns:
        if col_name.lower() == "user_id" or col_name.lower() == "index":
            continue
        if "date" in data_type:
            user_data[col_name] = st.date_input(f"Enter new {col_name}")
        elif "int" in data_type:
            user_data[col_name] = st.number_input(f"Enter new {col_name}", step=1)
        else:
            user_data[col_name] = st.text_input(f"Enter new {col_name}")
    
    if st.button("Update User"):
        update_query = ", ".join([f"{col} = %s" for col in user_data.keys()])
        query = f"""
        UPDATE user_profile_data
        SET {update_query}
        WHERE user_id = %s
        """
        execute_query(query, conn, tuple(user_data.values()) + (selected_username,))
        st.success("User updated successfully!")

