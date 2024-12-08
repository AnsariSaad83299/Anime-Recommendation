import streamlit as st

content_based = st.Page("content_based.py", title="Content Based Recommendation")
home = st.Page("home.py", title = "Home")
random_forest = st.Page("random_forest.py", title="Random Forest Analysis")
demographic = st.Page("demographic.py", title="Demographic based")
login = st.Page("login_page.py", title="Login Page")
signup = st.Page("signup_page.py", title="Signup new user")
favourites = st.Page("favourites_page.py", title="Favourites")
collaborative = st.Page("collaborative_svd.py", title="Collaborative Recommendation")
admin = st.Page("admin.py", title="Admin Page")

if "username" in st.session_state and st.session_state["username"]:
    st.navigation(
        [home, content_based, random_forest, demographic, collaborative, favourites, admin]
    ).run()
else:
    st.navigation(
        [login, signup]
    ).run()
