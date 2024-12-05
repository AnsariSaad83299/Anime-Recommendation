import pandas as pd
from sqlalchemy import create_engine

# Load CSV
csv_file = "anime-dataset-2023-preprocessed.csv"
df = pd.read_csv(csv_file)

df.rename(columns={
    'Name': 'name',
    'English name': 'english_name',
    'Other name': 'other_name',
    'Score': 'score',
    'Genres': 'genres',
    'Synopsis': 'synopsis',
    'Type': 'type',
    'Episodes': 'episodes',
    'Aired': 'aired',
    'Premiered': 'premiered',
    'Status': 'status',
    'Producers': 'producers',
    'Licensors': 'licensors',
    'Studios': 'studios',
    'Source': 'source',
    'Duration': 'duration',
    'Rating': 'rating',
    'Rank': 'rank',
    'Popularity': 'popularity',
    'Favorites': 'favorites',
    'Scored By': 'scored_by',
    'Members': 'members',
    'Image URL': 'image_url'
}, inplace=True)

df = df.drop(columns=['Start Date', 'End Date', 'Ongoing', 'Episodes_Normalized'])

# Database connection
db_connection = "postgresql://postgres:pgsql@localhost:5432/anime-recommendation"
engine = create_engine(db_connection)

# Insert data into the table
df.to_sql('anime', engine, if_exists='append', index=False)
