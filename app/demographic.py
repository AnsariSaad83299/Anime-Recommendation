import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from load_dataset import user_df_filtered, ratings_df, matching_columns_anime, anime_features_df
import joblib

st.title("Demographic-Based Anime Recommendation")

age = st.number_input("Enter Age", min_value=10, max_value=100, value=25)
gender = st.selectbox("Select Gender", ["Male", "Female", "Non-Binary"])
location = st.selectbox("Select Location", ['Australia', 
    'Brazil','Canada','France','Germany','Philippines','Poland','Russia','Sweden','United States'])

_mean = 32.76650026
_var = 4.4105517

user = pd.DataFrame({
    'Gender_Female':[int(gender=="Female")],
    'Gender_Male':[int(gender=="Male")], 
    'Gender_Non-Binary':[int(gender=="Non-Binary")], 
    'Location_Australia':[int(location=="Australia")], 
    'Location_Brazil':[int(location=="Brazil")], 
    'Location_Canada':[int(location=="Canada")], 
    'Location_France':[int(location=="France")], 
    'Location_Germany':[int(location=="Germany")], 
    'Location_Philippines':[int(location=="Philippines")], 
    'Location_Poland':[int(location=="Poland")], 
    'Location_Russia':[int(location=="Russia")], 
    'Location_Sweden':[int(location=="Sweden")], 
    'Location_United States':[int(location=="United States")], 
    'Age':[(age-_mean)/_var]
    })

knn_loaded = joblib.load('./models/knn_model_demo.pkl')
distances, indices = knn_loaded.kneighbors(user)
similar_user_ids = user_df_filtered.iloc[indices[0]]["mal_id"].values
similar_users_ratings = ratings_df[ratings_df['user_id'].isin(similar_user_ids)][["anime_id", "rating"]]


def calculate_relevance(anime_id, similar_users_ratings):
    anime_ratings = similar_users_ratings[similar_users_ratings['anime_id'] == anime_id]
    return anime_ratings['rating'].mean()

def calculate_diversity(selected_animes, anime_id, anime_feature_df):
    if not selected_animes:
        return 0
    
    candidate_features = anime_feature_df.loc[anime_features_df[anime_features_df['anime_id'] == anime_id].index].values.reshape(1, -1)
    selected_features = anime_feature_df.loc[anime_features_df[anime_features_df['anime_id'].isin(selected_animes)].index].values
    diversity_score = cosine_similarity(candidate_features, selected_features).mean()
    return diversity_score

def recommend_top_animes(similar_users_ratings, anime_feature_df, num_recommendations=10, alpha=0.7):
    candidate_animes = similar_users_ratings['anime_id'].unique()
    selected_animes = []
    mmr_scores = {}

    for _ in range(num_recommendations): 
        best_anime = None
        best_score = -np.inf

        for anime_id in candidate_animes:
            if anime_id in selected_animes:
                continue
            
            relevance = calculate_relevance(anime_id, similar_users_ratings)
            diversity = calculate_diversity(selected_animes, anime_id, anime_feature_df)

            mmr_score = alpha * relevance - (1 - alpha) * diversity

            if mmr_score > best_score:
                best_score = mmr_score
                best_anime = anime_id
        
        if best_anime is not None:
            selected_animes.append(best_anime)
            mmr_scores[best_anime] = best_score

    return selected_animes

if st.button("Get Recommendations"):
    top_animes = recommend_top_animes(similar_users_ratings, anime_features_df[matching_columns_anime], num_recommendations=10, alpha=0.7)
    top_animes_df = anime_features_df.loc[anime_features_df[anime_features_df['anime_id'].isin(top_animes)].index][["name","genres", "image_url"]].reset_index(drop=True)
    st.write("Recommended Animes:")
    for i in range(0, 10, 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < 10:
                with col:
                    row = top_animes_df.iloc[i + j]
                    st.image(row['image_url'], caption=f"{row['name']}: {row['genres']}")
    st.write("These are given on the basis of these most similar users")
    st.table(user_df_filtered.iloc[indices[0]][["username","gender", "age", "location"]])