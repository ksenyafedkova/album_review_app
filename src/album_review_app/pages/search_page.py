import streamlit as st
from album_review_app.ui import hide_sidebar_navigation, show_user_sidebar
from album_review_app.spotify_api import search_
from album_review_app.album_page import show_album_page
from album_review_app.logger import logger

from album_review_app.backend.db_request import (save_album_to_shelf)

hide_sidebar_navigation()
show_user_sidebar()

def show_search_page():
    artist_or_album = st.selectbox(
        'What would you like to search?',
        ['Album', 'Artist', 'Album and Artist'],
        index=None
    )

    if st.session_state.get('return_to_search'):
        search_value = st.session_state.get('last_search', '')
        st.session_state['return_to_search'] = False
    else:
        search_value = ''

    search_string = st.text_input(
        'Write the title of the Album and/or the name of the Artist',
        value=search_value
    )

    if search_string:
        if st.button('Search'):
            if artist_or_album == 'Album':
                # positive = 0
                # negative = 0
                # for _ in range(1):
                #     result_album = search_(album=search_string)
                #     if result_album.get('albums', 0):
                #         positive += 1
                #     else:
                #         negative += 1
                # st.success(f'Positive: {positive}')
                # st.error(f'Negative: {negative}')
                # st.write(result_album)
                try:
                    result_album = search_(album=search_string)
                    st.session_state['albums'] = result_album['albums']['items']
                    st.session_state['last_search'] = search_string
                except Exception as e:
                    logger.error(
                        f'Search failed for query '
                        f'{search_string}: {e}'
                    )
                    st.error('Something went wrong. Please try again later.')
                    st.stop()

        if (
                'albums' in st.session_state
                and st.session_state.get('last_search') == search_string
        ):
            for album in st.session_state['albums']:
                col1, col2 = st.columns([1, 4])

                with col1:
                    st.image(
                        album['images'][0]['url'],
                        width=150
                    )
                    if st.button(
                            "Open album",
                            key=f"album_{album['id']}"
                    ):
                        st.query_params["album"] = album["id"]
                        st.rerun()

                with (col2):
                    st.subheader(album['name'])
                    artists = ', '.join(
                        artist['name']
                        for artist in album['artists']
                    )

                    st.write(f'**{artists}**')
                    st.write(f"Released: {album['release_date']}")

                    with st.expander('Learn more'):
                        st.write(f"Album type: {album['album_type']}")
                        st.write(f"Tracks: {album['total_tracks']}")

                    col_a, col_b = st.columns(2)

                    with col_a:
                        if st.button(
                            "➕ Add to my shelf",
                            key=f"shelf_{album['id']}"
                        ):
                            try:
                                added = save_album_to_shelf(
                                    st.session_state['user_id'],
                                    album
                                )

                                if added:
                                    st.success('Added!')
                                else:
                                    st.info('This album is already on your shelf.')


                            except Exception as e:

                                st.error(f'Could not add album to your shelf: {e}')

                                logger.error(f'Add to shelf failed: {e}')


                    with col_b:
                        st.button(
                            "✏️ Write a review",
                            key=f"review_{album['id']}"
                        )

                        st.divider()







            # if artist_or_album == 'Artist':
            #     result_artist = search_(artist=search_string)
            #     st.write(result_artist)
            #
            # if artist_or_album == 'Album and Artist':
            #     result_album_artist = search_(search_string)



album_id = st.query_params.get("album")

if album_id:
    show_album_page(album_id)
else:
    show_search_page()