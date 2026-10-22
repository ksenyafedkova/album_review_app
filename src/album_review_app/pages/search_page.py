import streamlit as st
from album_review_app.ui import hide_sidebar_navigation, show_user_sidebar
from album_review_app.spotify_api import SpotifyClient
from album_review_app.album_page import show_album_page
from album_review_app.logger import logger

from album_review_app.backend.v1.api_script import save_album_to_shelf
from album_review_app.backend.schemes.schemes import SpotifyAlbum, SpotifyArtist

hide_sidebar_navigation()
show_user_sidebar()

spotify = SpotifyClient()

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
                try:
                    result_album = spotify.search(album=search_string)
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
                                album_data = SpotifyAlbum(
                                    spotify_id=album["id"],
                                    name=album["name"],
                                    release_date=album["release_date"],
                                    release_date_precision=album["release_date_precision"],
                                    cover_url=album["images"][0]["url"],
                                    artist=SpotifyArtist(
                                        spotify_id=album["artists"][0]["id"],
                                        name=album["artists"][0]["name"]
                                    )
                                )

                                added = save_album_to_shelf(
                                    st.session_state["user_id"],
                                    album_data
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
            #     result_artist = spotify.search(artist=search_string)
            #     st.write(result_artist)
            #
            # if artist_or_album == 'Album and Artist':
            #     result_album_artist = spotify.search(search_string)



album_spotify_id = st.query_params.get("album")

if album_spotify_id:
    show_album_page(album_spotify_id)
else:
    show_search_page()