import streamlit as st
import pandas as pd
from connector import sqlalchecmy_engine

if st.button("Logout"):
    st.session_state["username"] = ""

st.markdown("# Home page")
st.write("The animes in our database---->")

def fetch_df():
    query = "SELECT anime_id, name, score FROM anime LIMIT 30"
    df = pd.read_sql(query, sqlalchecmy_engine)
    return df

df = fetch_df()
st.dataframe(df, use_container_width=True)
