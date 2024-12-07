# Collbarative Filtering based on users who have rated other animes using SVD Matrix Factorization

import streamlit as st
import pandas as pd
import psycopg2
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split


st.markdown("# Collaborative Filtering based on other users' rated animes Page")

st.write('We are using the Animes that other users has rated to run \
        collaboratibe filtering recommendation algorithm which is based on SVD Matrix Factorization.')

if "username" in st.session_state and st.session_state["username"]:
    username = st.session_state["username"]
    st.success(f"Hello, {username}!")

    conn = psycopg2.connect(
        host="localhost",  # e.g., "localhost" or your DB server IP
        database="anime-recommendation",  # e.g., "test_db"
        user="postgres",  # e.g., "admin"
        password="pgsql",  # e.g., "password"
        port="5432"  # Default PostgreSQL port
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Write your SQL query
    query = "SELECT username, anime_title, rating FROM existing_users;"  # Modify with your actual query

    # Execute the query
    cursor.execute(query)

    # Fetch all rows from the table
    rows = cursor.fetchall()

    # Get column names from cursor description
    columns = ['Username', 'Anime Title', 'rating']

    # Convert rows to a pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Close cursor and connection
    cursor.close()
    conn.close()

    conn = psycopg2.connect(
    dbname="anime-recommendation",
    user="postgres",
    password="pgsql",
    host="localhost",
    port="5432"
    )
    cur = conn.cursor()
    cur.execute('''
        SELECT f.username, a.name, f.rating
        FROM favorites f
        JOIN anime a ON f.anime_id = a.anime_id
        WHERE f.username = %s
    ''', (username,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
  
    # Convert favorites to a pandas DataFrame
    df_currentuser = pd.DataFrame(rows, columns=['Username', 'Anime Title', 'rating'])

    df = pd.concat([df_currentuser, df], ignore_index=True)

    reader = Reader(rating_scale=(1, 5))

# Load the dataset into Surprise
    data = Dataset.load_from_df(df[['Username', 'Anime Title', 'rating']], reader)

    # Train-test split
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    # Initialize the SVD model
    model = SVD()

    # Train the model
    model.fit(trainset)

    def recommend_animes(model, user_name, anime_names, df, n=5):
    # Get animes the user has already rated
        rated_animes = df[df['Username'] == user_name]['Anime Title'].unique()

        # Filter out rated animes
        potential_animes = [anime for anime in anime_names if anime not in rated_animes]

        # Predict ratings for all potential animes
        predictions = [(anime_name, model.predict(user_name, anime_name).est) for anime_name in potential_animes]

        # Sort by predicted rating in descending order
        recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]

        return recommendations

    # Get all unique anime IDs
    all_anime_names = df['Anime Title'].unique()

    # Recommend top 5 animes for user_id=saad123
    recommendations = recommend_animes(model, user_name=username, anime_names=all_anime_names, df=df, n=5)

    recommendations_df =  pd.DataFrame(recommendations, columns=['Anime Title', 'Predicted Rating'])

    st.write('We recommended these animes:')

    st.dataframe(recommendations_df, use_container_width=True)

    

else:
    st.write("Please Log In")