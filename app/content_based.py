import streamlit as st
from connector import sqlalchecmy_engine, get_db_connection
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler, OneHotEncoder
import joblib

st.markdown("# Content Based Recommendation Page")

st.write('We are using the Animes that a user has added to favourites to run \
        content based recommendation algorithm.')

if "username" in st.session_state and st.session_state["username"]:
    username = st.session_state["username"]
    st.success(f"Hello, {username}!")

    # Function to fetch a page of data using SQLAlchemy
    query = "SELECT * FROM anime"
    df = pd.read_sql(query, sqlalchecmy_engine)
    
    df.dropna(inplace=True)

    df = df.drop(df[df['type'] == 'UNKNOWN'].index)

    df = df.drop(df[df['source'] == 'Unknown'].index)

    df = df.drop(df[df['source'] == 'Other'].index)

    df.reset_index(drop=True, inplace=True)
    
    mlb = MultiLabelBinarizer()
    genres_encoded = mlb.fit_transform(df['genres'].str.split(', '))
    genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)

    genres_df.drop(columns=['UNKNOWN'], inplace=True)

    type_encoder = OneHotEncoder(sparse_output=False)
    type_encoded = type_encoder.fit_transform(df[['type']])
    type_df = pd.DataFrame(type_encoded, columns=type_encoder.get_feature_names_out(['type'])).astype(int)

    source_encoder = OneHotEncoder(sparse_output=False)
    source_encoded = source_encoder.fit_transform(df[['source']])
    source_df = pd.DataFrame(source_encoded, columns=source_encoder.get_feature_names_out(['source'])).astype(int)

    scaler = StandardScaler()
    df['episodes'] = scaler.fit_transform(df[['episodes']])

    features = pd.concat([genres_df, type_df, source_df, df['episodes']], axis=1)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT f.anime_id, f.rating
        FROM favorites f
        JOIN anime a ON f.anime_id = a.anime_id
        WHERE f.username = %s
    ''', (username,))
    favorites = cur.fetchall()
    cur.close()
    conn.close()
    user_input = pd.DataFrame(favorites, columns=["Anime ID", "Rating"])
    
    user_anime_features = features.loc[df.loc[df['anime_id'].isin(user_input['Anime ID'])].index]

    user_ratings = np.array(user_input["Rating"])

    user_preference_vector = np.average(user_anime_features, axis=0, weights=user_ratings)

    knn = joblib.load('models/knn_model_content.pkl')

    distances, indices = knn.kneighbors([user_preference_vector])
    matching_score = (1- distances[0])*100
    recommendations = df.iloc[indices[0]]
    st.dataframe(recommendations, use_container_width=True)

else:
    st.write("Please Log In")