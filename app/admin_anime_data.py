import pandas as pd
import streamlit as st

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

def get_row_by_id(conn, anime_id):
    query = "SELECT * FROM clean_anime_data WHERE anime_id = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (anime_id,))
        row = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]
    return dict(zip(column_names, row)) if row else None

def execute_query(query, conn, params=None):
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        conn.commit()

def get_ids(conn):
    query = f"SELECT anime_id FROM clean_anime_data"
    with conn.cursor() as cursor:
        cursor.execute(query)
        ids = [row[0] for row in cursor.fetchall()]
    return ids

def create_anime(conn):
    st.header("Create Anime Data")

    columns = get_table_columns(conn, "clean_anime_data")

    anime_data = {}
    for col_name, data_type in columns:
        if col_name.lower() == "anime_id":
            continue
        if "date" in data_type:
            anime_data[col_name] = st.date_input(f"Enter {col_name}")
        elif "int" in data_type:
            anime_data[col_name] = st.number_input(f"Enter {col_name}", step=1)
        else:
            anime_data[col_name] = st.text_input(f"Enter {col_name}")

    if st.button("Create Anime"):
        column_names = ", ".join(anime_data.keys())
        placeholders = ", ".join(["%s"] * len(anime_data))
        query = f"INSERT INTO cleaned_anime_data ({column_names}) VALUES ({placeholders})"
        
        execute_query(query, conn, tuple(anime_data.values()))
        st.success("Anime data created successfully!")

def read_anime(conn):
    st.header("Read Cleaned Anime Data")
    
    query = "SELECT * FROM clean_anime_data LIMIT 10"
    df = pd.read_sql(query, conn)
    st.write(df)

    st.header("Get Particular Anime Data")
    anime_ids = get_ids(conn)
    selected_animeid = st.selectbox("Select Anime ID", anime_ids, key="select_user_read")

    if selected_animeid:
        anime_details = get_row_by_id(conn, selected_animeid)
        if anime_details:
            st.subheader("Anime Details")
            st.table(anime_details)
        else:
            st.warning("User not found.")

def delete_anime(conn):
    st.header("Delete Anime Data")
    
    anime_ids = get_ids(conn)
    selected_anime_id = st.selectbox("Select Anime ID to Update", anime_ids)
    
    if st.button("Delete Anime"):
        query = "DELETE FROM clean_anime_data WHERE anime_id = %s"
        execute_query(query, conn, (selected_anime_id,))
        st.success("Anime deleted successfully!")

def update_anime(conn):
    st.header("Update Anime Data")
    anime_ids = get_ids(conn)
    selected_anime_id = st.selectbox("Select Anime ID to Update", anime_ids)

    columns = get_table_columns(conn, "clean_anime_data")

    anime_data = {}
    for col_name, data_type in columns:
        if col_name.lower() == "anime_id" or col_name.lower()=="index":
            continue
        if "date" in data_type:
            anime_data[col_name] = st.date_input(f"Enter new {col_name}")
        elif "int" in data_type:
            anime_data[col_name] = st.number_input(f"Enter new {col_name}", step=1)
        else:
            anime_data[col_name] = st.text_input(f"Enter new {col_name}")

    if st.button("Update Anime"):
        update_query = ", ".join([f"{col} = %s" for col in anime_data.keys()])
        query = f"""
        UPDATE cleaned_anime_data
        SET {update_query}
        WHERE anime_id = %s
        """
        execute_query(query, conn, tuple(anime_data.values()) + (selected_anime_id,))
        st.success("Anime updated successfully!")