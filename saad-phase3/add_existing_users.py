import psycopg2
import pandas as pd

# Assuming your dataframe is already loaded
df = pd.read_csv('users-score.csv')  

df['rating'] = ((df['rating'] - 1) / (10 - 1)) * (5 - 1) + 1

# Round to 2 decimal places for better readability
df['rating'] = df['rating'].round()

# Database connection parameters
db_config = {
    "dbname": "anime-recommendation",
    "user": "postgres",
    "password": "pgsql",
    "host": "localhost",  # or your database host
    "port": 5432          # default PostgreSQL port
}

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Insert each record from the DataFrame into the `favorites` table
    insert_query = """
    INSERT INTO existing_users (username, anime_id, anime_title, rating)
    VALUES (%s, %s, %s, %s)
    """  # Adjust ON CONFLICT as needed if unique constraints are applied
    
    for _, row in df.iterrows():
        cursor.execute(insert_query, (row["Username"], row["anime_id"], row["Anime Title"], row["rating"]))
    
    # Commit the changes
    conn.commit()

    print("Data inserted successfully.")

except Exception as e:
    print("An error occurred:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
