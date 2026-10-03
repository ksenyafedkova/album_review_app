import streamlit as st
from album_review_app.ui import hide_sidebar_navigation, show_user_sidebar
from album_review_app.backend.db_request import get_user_albums, delete_from_shelf
from album_review_app.logger import logger
from album_review_app.album_page import show_album_page

hide_sidebar_navigation()
show_user_sidebar()

username = st.session_state['username']

def show_home_page():
    user_albums = get_user_albums(username)

    for album in user_albums:
        col1, col2 = st.columns([1, 4])

        with col1:
            st.image(
                album['cover_url'],
                width=150
            )
            if st.button(
                    "Open album",
                    key=f"album_{album['id']}"
            ):
                st.query_params["album"] = album["spotify_id"]
                st.rerun()

        with (col2):
            st.subheader(album['name'])
            st.write(f'**{album['artist_name']}**')
            st.write(f'Released: {album['release_date']}')

            col_a, col_b, col_c = st.columns(3)
            with col_c:
                if st.button(
                    label="Delete from my shelf: 🗑️",
                    key=f'delete_from_my_shelf_{album['id']}'
                ):
                    try:
                        delete_from_shelf(st.session_state['user_id'], album['id'])
                        st.rerun()

                    except Exception as e:

                        st.error(f'Could not delete album from your shelf: {e}')

                        logger.error(f'Delete from shelf failed: {e}')

            st.divider()

            # with st.expander('Learn more'):
            #     st.write(f'Album type: {album['album_type']}')
            #     st.write(f'Tracks: {album['total_tracks']}')

    if st.button('Find an album!'):
        st.switch_page('pages/search_page.py')

album_id = st.query_params.get("album")

if album_id:
    show_album_page(album_id)
else:
    show_home_page()