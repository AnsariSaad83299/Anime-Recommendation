CREATE TABLE anime (
    index INT,
    anime_id INT PRIMARY KEY,
    name TEXT,
    english_name TEXT,
    other_name TEXT,
    score TEXT,
    genres TEXT,
    synopsis TEXT,
    type TEXT,
    episodes TEXT,
    aired TEXT,
    premiered TEXT,
    status TEXT,
    producers TEXT,
    licensors TEXT,
    studios TEXT,
    source TEXT,
    duration TEXT,
    rating TEXT,
    rank TEXT,
    popularity INT,
    favorites INT,
    scored_by TEXT,
    members INT,
    image_url TEXT,
    start_date DATE,
    end_date DATE,
    ongoing INT NOT NULL,
    episodes_normalized FLOAT
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE favorites (
    favorite_id SERIAL PRIMARY KEY,
    username VARCHAR REFERENCES users(username) ON DELETE CASCADE,
    anime_id INT REFERENCES anime(anime_id) ON DELETE CASCADE,
    rating INT
);

CREATE TABLE clean_anime_data (
    index INT PRIMARY KEY,
    anime_id INT NOT NULL,
    name TEXT NOT NULL,
    english_name TEXT NOT NULL,
    other_name TEXT NOT NULL,
    score TEXT NOT NULL,
    genres TEXT NOT NULL,
    synopsis TEXT NOT NULL,
    type TEXT NOT NULL,
    episodes FLOAT,
    aired TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    premiered TEXT NOT NULL,
    status TEXT NOT NULL,
    producers TEXT NOT NULL,
    licensors TEXT NOT NULL,
    studios TEXT NOT NULL,
    source TEXT NOT NULL,
    duration TEXT NOT NULL,
    rating TEXT NOT NULL,
    rank TEXT NOT NULL,
    popularity INT NOT NULL,
    favorites INT NOT NULL,
    scored_by TEXT NOT NULL,
    members INT NOT NULL,
    image_url TEXT NOT NULL,
    ongoing INT NOT NULL,
    episodes_norm FLOAT
);

CREATE TABLE user_anime_rating_data (
    index INT PRIMARY KEY,
    user_id INT NOT NULL,
    anime_id INT NOT NULL,
    rating INT NOT NULL,
    gender TEXT,
    location TEXT,
    birthday_date TEXT,
    joined_date TEXT,
    age_join FLOAT,
    episodes_watched FLOAT,
    age FLOAT,
    name TEXT NOT NULL,
    genres TEXT,
    type TEXT,
    start_date TEXT,
    end_date TEXT,
    studios TEXT,
    source TEXT,
    rank TEXT,
    episodes FLOAT,
    episodes_norm FLOAT
);


CREATE TABLE user_profile_data (
    index INT PRIMARY KEY,
    mal_id INT NOT NULL,
    username TEXT NOT NULL,
    gender TEXT,
    birthday TEXT NOT NULL,
    location TEXT NOT NULL,
    joined TEXT NOT NULL,
    days_watched FLOAT,
    mean_score FLOAT,
    watching FLOAT,
    completed FLOAT,
    on_hold FLOAT,
    dropped FLOAT,
    plan_to_watch FLOAT,
    total_entries FLOAT,
    rewatched FLOAT,
    episodes_watched FLOAT,
    birthday_date TEXT NOT NULL,
    joined_date TEXT NOT NULL,
    age_join FLOAT NOT NULL
);

