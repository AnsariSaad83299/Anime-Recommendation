# Anime-Recommendation

In this project we are working on creating a anime recommendation engine using user watch history and demographic data like user's location, age and gender. We have created a app in using streamlit which can be found under the app directory.

## Team members:
| Name | UB Number | Email |
| :---: | :---: | :---: |
| Saad Ansari | 50607542| mohdsaad@buffalo.edu |
| Seokwoo Park | 50608072 | seokwoop@buffalo.edu |
| Ramachandran Kulothungan | 50611273 | rkulothu@buffalo.edu |
| Rutuja Badve | 50604168 | rutujara@buffalo.edu | 

## Description:
In recommendation of an anime there are two scenarios: 
- we have a completely new person who hasn't watched any anime
- we have a person who has already seen a few anime and wants to watch new anime

In most anime streaming websites like Crunchyroll, torrent sites like zorotv we do not have proper suggestions based on either of these.
They mostly have generic recommendations like top airing, top watched, top rated etc. We want to provide a more personalised experience to a person
so that they have the best anime experience.

We are building a recommendation engine that can work on either scenario. We have used a dataset available in Kaggle which is created by scraping data from MyAnimeList

### Highlights:
- We have a demographic-based recommendation system that takes a user's age, gender, and location to determine the best anime based on the animes watched by users with a similar demographic. This system also tries to provide a varied range of animes so that a new user can be introduced to diverse animes to explore.

- We have a content-based recommendation system that suggests the best animes that are similar to previously viewed anime based on similarity. We take the input the animes the user has watched and their corresponding rating. We then calculate `user_preference_vector` which is the weighted average of the features of anime based on the ratings. Hence the animes rated lower have low contribution to the recommendation of new animes. We use KNN to find similar animes and the similarity metric is cosine similarity

- We have a collaborative recommendation system that identifies similar users on the basis of previous commonly watched animes to suggest new animes to the target user that are famous among the other users with similar tastes.

- We have done extensive data cleaning to get user's location as they were not directly available. The location field had entries with just state in a country, or even country names in multiple formats like two letter codes, three letter codes, complete names, alternate names.

## File Structure
We have multiple Notebooks that currently serve different purposes.

data_fetching.ipynv: Downloads the dataset files from Kaggle and stores them in datasets directory.

data_cleaning.ipynb: Contains various steps for cleaning the dataset considering various factors and conditions and store the cleaned datasets in cleaned_datsets directory. 

Our Individual Scripts and reports are added to the **individual_scripts** folder

## Steps to deploy the App:
To launch the app you need to have postgres and the required packages installed.

### Install Packages
To install the reuired packages, create a python(3.12 used by us) virtual environment and activate it. Then execute from the anime-recommendation repo root directory:
```
pip install -r requirements.txt
```

### Setup Database
We have used postgres@17, create a database with name: anime-recommendation.
Update the file app/connector.py with your username and password for postgresql anime-recommendation database user.

### Seed data to database
You would need to seed the data that we used into your database. We have created two scripts to make the process straighforward.

#### Create tables
app/setup/db.sql: Run this SQL script to create the required table with the correct schema. 
You can use the following command to do this. Remember to update your username in the command.
```
psql -U {username} -d "anime-recommendation" -a -f app/setup/db.sql
```

#### Load data from the CSVs
We need the data used to train our model to be available in the database to be able to use the predictions.
You can download the datasets from: https://drive.google.com/file/d/1FHEQVYllCuk25abFE4bbBOIYVXtBvXG7/view?usp=sharing
This zip file has two directories: cleaned_datasets and joined_datasets

Extract the zip and store it in the Anime-recommendation repo root directory.
Expected folder structure:

- anime-recommendation
  - app
  - models
  - cleaned_datasets
  - joined_datasets
  - individual_scripts
  - README.md
  - requirements.txt 

Now execute the app/setup/seed_data.py script. Make sure to update the app/connector.py with your postgres user's username and password before running the seed script.

You can execute it with this command from anime-recommendation repo root directory:
```
PYTHONPATH=./app python app/setup/seed_data.py
```

### Deploy the app:
Once all packages and tables are setup, you can launch the streamlit app by running this command from anime-recommendation repo root directory:
```
PYTHONPATH=./app streamlit run app/app.py
```
You should now be able to access the site at: http://localhost:8501


## Mohd Saad Mohd Intesar Ansari (50607542):
- **Question 1:** Do people like long animes or short animes?
- **Question 2:** which Genres are the most popular?
- **Code Location:** `individual_scripts/Saad/MohdSaad_50607542_phase2.ipynb` and `individual_scripts/Saad/MohdSaad_50607542_phase2.pdf`

## Ramachandran Kulothungan  (50611273):
- **Question 1:** Does user's demographic(location, age, gender) impact type of anime(genre, episodes, anime type(OVA, movie), Rank) they are prefer?
- **Question 2:** Can we identify users who have similar viewing habits and recommend anime based on these similarities?
- **Files:**
  -   **Phase1** [EDA]([https://duckduckgo.com](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_EDA.ipynb)), [Report](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_EDA.pdf)
  -   **Phase2**
    - [Additional EDA](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_EDA_additional.ipynb),[Additional EDA report](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_EDA_additional.pdf)
    - [Question 1 Analysis- Algo 1](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis1.ipynb), [Question 1 Analysis Report- Algo 1](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis1.pdf)
    - [Question 1 Analysis- Algo 2](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis2.ipynb), [Question 1 Analysis Report- Algo 2](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis2.pdf)
    - [Question 2 Analysis- Algo 1](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis3.ipynb), [Question 2 Analysis Report- Algo 1](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis3.pdf)
    - [Question 2 Analysis- Algo 2](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis4.ipynb), [Question 2 Analysis Report- Algo 2](https://github.com/AnsariSaad83299/Anime-Recommendation/blob/main/individual_scripts/RC/RC_ML_Analysis4.pdf)

## Rutuja Badve (50604168):
- **Question 1:** Do different age groups prefer anime with varying durations?
- **Question 2:** Does the number of episodes affect the score of anime?
- **Code Location:** individual_scripts/Rutuja/RutujaBadve_50604168_phase2.ipynb and individual_scripts/Rutuja/RutujaBadve_50604168_phase2.pdf
- **Analysis for Question1:** page 2 and page 3 of individual_scripts/Rutuja/RutujaBadve_50604168_phase2.pdf
- **Analysis for Question2:** page 5 and page 6 of individual_scripts/Rutuja/RutujaBadve_50604168_phase2.pdf
SW Park
11:41 PM
Phase2_Problem1_50608072.ipynb
Phase2_Problem2_50608072.ipynb
SW Park
11:51 PM
## Seokwoo Park (50608072):
- **Question 1:** By training Collaborative Filtering on specific anime ratings, I can predict how users with similar tastes would rate them.
- **Question 2:** The completion rate ('Completed / Total Entries') is expected to increase with both higher age group concentrations and longer Days Watched values.
- **Code Location:** `individual_scripts/Park/Phase2_Problem1_50608072.ipynb` and `individual_scripts/Saad/Phase2_Problem2_50608072.ipynb`
