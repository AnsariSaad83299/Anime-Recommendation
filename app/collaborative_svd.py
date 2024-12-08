from connector import sqlalchecmy_engine, get_db_connection
import streamlit as st
import pandas as pd
import psycopg2
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split


st.markdown("# Collaborative Filtering based on other users' rated animes Page")

st.write('We are using the Animes that other users has rated to run \
        collaboratibe filtering recommendation algorithm which is based on SVD Matrix Factorization.')

username = st.session_state["username"]
st.success(f"Hello, {username}!")

conn = get_db_connection()
cursor = conn.cursor()
query = "SELECT user_id, name, rating FROM user_anime_rating_data;"

cursor.execute(query)

rows = cursor.fetchall()

columns = ['Username', 'Anime Title', 'rating']

df = pd.DataFrame(rows, columns=columns)

cursor.close()
conn.close()

conn = get_db_connection()
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

df_currentuser = pd.DataFrame(rows, columns=['Username', 'Anime Title', 'rating'])

df = pd.concat([df_currentuser, df], ignore_index=True)

reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(df[['Username', 'Anime Title', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

model = SVD()

model.fit(trainset)

def recommend_animes(model, user_name, anime_names, df, n=5):

    rated_animes = df[df['Username'] == user_name]['Anime Title'].unique()


    potential_animes = [anime for anime in anime_names if anime not in rated_animes]


    predictions = [(anime_name, model.predict(user_name, anime_name).est) for anime_name in potential_animes]


    recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]

    return recommendations


all_anime_names = df['Anime Title'].unique()


recommendations = recommend_animes(model, user_name=username, anime_names=all_anime_names, df=df, n=5)

recommendations_df =  pd.DataFrame(recommendations, columns=['Anime Title', 'Predicted Rating'])

st.write('We recommended these animes:')

st.dataframe(recommendations_df, use_container_width=True)
