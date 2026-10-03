import streamlit as st
from auth import login_user
from ui import hide_sidebar_navigation

hide_sidebar_navigation()

st.set_page_config(page_title="Album Review App", page_icon="💿")


st.header('Welcome to the Album Review App')

st.image('src/memes/sponge_bob_floating.jpg', width=300)

login_user()

if st.session_state.get("logged_in"):
    st.switch_page('src/pages/home_page.py')

if st.button("Don't have an account? Sign up!"):
    st.switch_page('src/pages/register.py')