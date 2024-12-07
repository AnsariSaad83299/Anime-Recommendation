import pandas as pd
import numpy as np
from connector import sqlalchecmy_engine

query = "SELECT user_id, anime_id, rating FROM user_anime_rating_data"
ratings_df = pd.read_sql(query, sqlalchecmy_engine)
query = "SELECT mal_id, username, gender, location, birthday_date FROM user_profile_data"
user_df = pd.read_sql(query, sqlalchecmy_engine)
query = "SELECT anime_id, name, image_url, genres, type, episodes_norm FROM clean_anime_data"
anime_df = pd.read_sql(query, sqlalchecmy_engine)

top_countries = user_df['location'].value_counts().head(10)
top_10_countries = top_countries.index.tolist()
user_df_filtered = user_df[user_df['location'].isin(top_10_countries)]
user_df_filtered["age"] = ((pd.to_datetime('Jan 01, 2024', format='%b %d, %Y') - pd.to_datetime(user_df_filtered["birthday_date"], format='%Y-%m-%d')) / np.timedelta64(52, 'W')).round()

from sklearn.preprocessing import MultiLabelBinarizer

anime_df_one_hot = pd.get_dummies(anime_df, columns=['type'])
anime_df_one_hot
anime_df_one_hot['genres'] = anime_df_one_hot['genres'].str.strip().str.replace(', ', ',').str.replace(' ,', ',').str.split(',')
mlb = MultiLabelBinarizer()
genres_one_hot = pd.DataFrame(mlb.fit_transform(anime_df_one_hot['genres']), columns=mlb.classes_, index=anime_df.index)
genres_one_hot = genres_one_hot.add_prefix("genres_")
genres_one_hot
anime_features_df = pd.concat([anime_df, genres_one_hot], axis=1)
anime_features_df
import re
features_columns_regex = [r"^genres_.*", r"^type_.*", r"^episodes_norm$"]

matching_columns_anime = []

for col in anime_features_df.columns:
    if any(re.match(pattern, col) for pattern in features_columns_regex):
        matching_columns_anime.append(col)