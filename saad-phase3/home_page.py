import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Streamlit markdown and description
st.markdown("# Home page")
st.write("The animes in our database---->")

# Set up SQLAlchemy engine
DATABASE_URL = "postgresql://postgres:pgsql@localhost/anime-recommendation"
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Function to fetch a page of data using SQLAlchemy
def fetch_df():
    query = "SELECT anime_id, name, score FROM anime LIMIT 30"
    df = pd.read_sql(query, engine)
    return df

# Display the first page of data
df = fetch_df()
st.dataframe(df, use_container_width=True)

# Close the session
session.close()


