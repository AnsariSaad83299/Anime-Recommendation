import pandas as pd
from connector import sqlalchecmy_engine as engine

csv_to_table = {
    "joined_datasets/joined_rating_dataset.csv": "user_anime_rating_data",
    "cleaned_datasets/users_details_dataset_cleaned.csv": "user_profile_data",
    "cleaned_datasets/anime_dataset_cleaned.csv": "clean_anime_data",
    "cleaned_datasets/anime-dataset-2023-preprocessed.csv": "anime"
}

def load_csv_to_db(csv_file, table_name, engine):
    try:
        print(f"Loading {csv_file} into table '{table_name}'...")
        df = pd.read_csv(csv_file)
        df.reset_index(inplace=True)
        if 'Unnamed: 0' in df.columns:
            df.drop(columns=['Unnamed: 0'], inplace=True)
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Successfully loaded '{csv_file}' into table '{table_name}'.")
    except Exception as e:
        print(f"Error loading '{csv_file}' into table '{table_name}': {e}")

for csv_file, table_name in csv_to_table.items():
        load_csv_to_db(csv_file, table_name, engine)
