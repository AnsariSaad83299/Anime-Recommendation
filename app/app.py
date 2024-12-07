import streamlit as st

logistic_page = st.Page("logistic.py", title="Check expected anime performance")
content_based = st.Page("content_based.py", title="Based on rated animes")
home = st.Page("home.py", title = "Home")
random_forest = st.Page("random_forest.py", title="Random Forest")
demographic = st.Page("demographic.py", title="Demographic based")
login = st.Page("login_page.py", title="Login Page")
signup = st.Page("signup_page.py", title="Signup new user")
favourites = st.Page("favourites_page.py", title="Favourites")
# favourites = st.Page("logout.py", title="Logout")

if "username" in st.session_state and st.session_state["username"]:
    st.navigation(
        [home, logistic_page, content_based, random_forest, demographic, favourites]
    ).run()
else:
    st.navigation(
        [login, signup]
    ).run()
