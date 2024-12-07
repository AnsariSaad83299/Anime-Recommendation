import streamlit as st
import psycopg2
import pandas as pd

st.markdown("# Favourites page")

def display_favorites(username):
    conn = psycopg2.connect(
        dbname="anime-recommendation",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute('''
        SELECT f.anime_id, a.name, f.rating
        FROM favorites f
        JOIN anime a ON f.anime_id = a.anime_id
        WHERE f.username = %s
    ''', (username,))
    favorites = cur.fetchall()
    cur.close()
    conn.close()
    if favorites:
    # Convert favorites to a pandas DataFrame
        df_favorites = pd.DataFrame(favorites, columns=["Anime ID", "Name", "Rating"])
        st.subheader("Your Favorite Animes")
        st.dataframe(df_favorites)  # Display the DataFrame
    else:
        st.info("You have no favorite animes.")
    

def add_favorites(username, anime_ids_input, ratings_input):
    anime_ids = list(map(int, anime_ids_input.split()))
    ratings = list(map(int, ratings_input.split()))
    conn = psycopg2.connect(
        dbname="anime-recommendation",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        for anime_id, rating in zip(anime_ids, ratings):
            cur.execute('''
                INSERT INTO favorites (username, anime_id, rating)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            ''', (username, anime_id, rating))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Error adding favorites: {e}")
        return False
    finally:
        cur.close()
        conn.close()
        st.write('added animes to favorite')
        st.rerun()

def delete_favorites(username, anime_ids_input):
    anime_ids = list(map(int, anime_ids_input.split()))
    conn = psycopg2.connect(
        dbname="anime-recommendation",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        # Execute delete query for each anime_id
        cur.executemany('''
            DELETE FROM favorites
            WHERE username = %s AND anime_id = %s
        ''', [(username, anime_id) for anime_id in anime_ids])
        conn.commit()
    except Exception as e:
        conn.rollback()
        st.error(f"Error deleting favorites: {e}")
    finally:
        cur.close()
        conn.close()
        st.rerun()


if "username" in st.session_state and st.session_state["username"]:
    username = st.session_state["username"]
    st.success(f"Hello, {username}!")

    display_favorites(username)
    
    st.subheader("Add New Favorites")
    anime_ids_input = st.text_input("Enter Anime IDs (separated by spaces)", key="add_anime_ids")
    ratings_input = st.text_input("Enter Ratings (1-5) for each Anime (separated by spaces)", key="add_ratings")

    if st.button("Add to Favorites", key="add_button"):
        add_favorites(username, anime_ids_input, ratings_input)

    st.subheader("Delete Favorites")
    anime_ids_input_for_deleting = st.text_input("Enter Anime IDs (separated by spaces)", key="delete_anime_ids")

    if st.button("Delete Favorites", key="delete_button"):
        delete_favorites(username, anime_ids_input_for_deleting)


else: 
    st.write("Please Log In")

