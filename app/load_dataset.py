import pandas as pd
import numpy as np

ratings_df = pd.read_csv('joined_datasets/joined_rating_dataset.csv')
user_df = pd.read_csv("cleaned_datasets/users_details_dataset_cleaned.csv")
anime_df = pd.read_csv("cleaned_datasets/anime_dataset_cleaned.csv")

top_countries = user_df['Location'].value_counts().head(10)
top_10_countries = top_countries.index.tolist()
user_df_filtered = user_df[user_df['Location'].isin(top_10_countries)]
user_df_filtered["Age"] = ((pd.to_datetime('Jan 01, 2024', format='%b %d, %Y') - pd.to_datetime(user_df_filtered["Birthday_Date"], format='%Y-%m-%d')) / np.timedelta64(52, 'W')).round()

from sklearn.preprocessing import MultiLabelBinarizer

anime_df_one_hot = pd.get_dummies(anime_df, columns=['Type'])
anime_df_one_hot
anime_df_one_hot['Genres'] = anime_df_one_hot['Genres'].str.strip().str.replace(', ', ',').str.replace(' ,', ',').str.split(',')
mlb = MultiLabelBinarizer()
genres_one_hot = pd.DataFrame(mlb.fit_transform(anime_df_one_hot['Genres']), columns=mlb.classes_, index=anime_df.index)
genres_one_hot = genres_one_hot.add_prefix("Genres_")
genres_one_hot
anime_features_df = pd.concat([anime_df, genres_one_hot], axis=1).drop('Genres', axis=1)
anime_features_df
import re
features_columns_regex = [r"^Genres_.*", r"^Type_.*", r"^Episodes_Norm$"]

matching_columns_anime = []

for col in anime_features_df.columns:
    if any(re.match(pattern, col) for pattern in features_columns_regex):
        matching_columns_anime.append(col)