import streamlit as st

logistic_page = st.Page("logistic.py", title="Check expected anime performance")
content_based = st.Page("content_based.py", title="Based on rated animes")
home = st.Page("home.py", title = "Home")
collaborative = st.Page("collaborative.py", title="Collaborative filtering")
demographic = st.Page("demographic.py", title="Demographic based")
test = st.Page("test_st.py", title="Test streamlit features")
st.navigation(
    [home, logistic_page, content_based, collaborative, demographic, test]
    ).run()
