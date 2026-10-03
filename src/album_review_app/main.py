import streamlit as st
from album_review_app.auth import login_user
from album_review_app.ui import hide_sidebar_navigation

import os

hide_sidebar_navigation()

st.set_page_config(page_title="Album Review App", page_icon="💿")


st.header('Welcome to the Album Review App')

st.image('memes/sponge_bob_floating.jpg', width=300)

login_user()

if st.session_state.get("logged_in"):
    st.switch_page('pages/home_page.py')

if st.button("Don't have an account? Sign up!"):
    st.switch_page('pages/register.py')