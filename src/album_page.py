import streamlit as st
from spotify_api import get_album_info_from_spotify


def show_album_page(album_id):
    if st.button("← Back"):
        st.session_state['return_to_search'] = True
        del st.query_params["album"]
        st.rerun()

    album_info = get_album_info_from_spotify(album_id)

    st.title(album_info['album_name'])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            album_info['cover_url'],
            width=300
        )

    with col2:
        st.subheader(album_info['artist'])

        st.write(
            f"**Released:** {album_info['release_date']}"
        )

        st.write(
            f"**Album type:** {album_info['album_type'].capitalize()}"
        )

        st.write(
            f"**Tracks:** {album_info['total_tracks']}"
        )

        st.link_button(
            "🎧 Open in Spotify",
            album_info['spotify_url']
        )

    st.divider()

    st.subheader("Tracklist")

    for track in album_info['tracks']:
        artists = ", ".join(track['artists'])

        st.write(
            f"**{track['number']}. {track['name']}** — {artists}"
        )


