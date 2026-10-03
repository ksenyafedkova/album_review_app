import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
import streamlit as st


load_dotenv()

def get_access_token():
    url = "https://accounts.spotify.com/api/token"

    headers = {
         "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }

    response = requests.post(url, data=data, headers=headers)
    response_data = response.json()
    token = response_data['access_token']
    expires_in = response_data['expires_in']
    token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
    token_data = {
        'access_token': token,
        'expires_at': token_expires_at
    }
    # print(response.json())
    # st.write("NEW TOKEN:", token)
    # st.write("EXPIRES AT:", token_expires_at)
    return token_data


response_from_api = {'access_token': 'BQBj08cuYTmhFSWnc5R9ZrFvS9e2Z9qVyyWhb4Lepkl5VhMks9dCc7JDrlnkZGySfxbFI9opMXOSfPqhiVMXD_aO6OTldw1IkY5rqx-HekRrFJNZznk9BtHu4G06rYp3HL8xbXWPV7Tl',
 'token_type': 'Bearer',
 'expires_in': 3600}
# print(get_access_token())


def get_album_info_from_spotify(album_id):
    url = f'https://api.spotify.com/v1/albums/{album_id}'
    if (
            'token_data' not in st.session_state
            or datetime.now() >= st.session_state.token_data['expires_at']
    ):
        st.session_state.token_data = get_access_token()

    token = st.session_state.token_data['access_token']

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    data = response.json()


    cover_url = data['images'][0]['url']
    album_name = data['name']
    release_date = data['release_date']
    artist_name = data['artists'][0]['name']
    artist_id = data['artists'][0]['id']
    album_type = data['album_type']
    total_tracks = data['total_tracks']
    tracks = data['tracks']['items']
    spotify_url = data['external_urls']['spotify']

    track_list = []

    for track in tracks:
        track_number = track['track_number']
        track_name = track['name']

        artists = []

        for artist in track['artists']:
            artists.append(artist['name'])

        track_list.append({
            'number': track_number,
            'name': track_name,
            'artists': artists
        })


    album_info = {
        'cover_url': cover_url,
        'album_name': album_name,
        'spotify_url': spotify_url,
        'release_date': release_date,
        'artist': artist_name,
        'artist_id': artist_id,
        'album_type': album_type,
        'total_tracks': total_tracks,
        'tracks': track_list

    }

    return album_info

# print(get_album('3WZZF72ihlKPZBS4zSsNHl'))


def search_(album='', artist=''):
    url = 'https://api.spotify.com/v1/search'
    if (
            'token_data' not in st.session_state
            or datetime.now() >= st.session_state.token_data['expires_at']
    ):
        st.session_state.token_data = get_access_token()

    token = st.session_state.token_data['access_token']


    if album and artist:
        params = {
            "q": f'album:{album} artist:{artist}',
            "type": "album",
            "limit": 10
        }


    elif album and not artist:
        params = {
            "q": f'album:{album}',
            "type": "album",
            "limit": 10
        }

    elif artist and not album:
        params = {
            "q": f'artist:{artist}',
            "type": "artist",
            "limit": 10
        }


    headers = {
            'Authorization': f'Bearer {token}'
        }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()
    return data



def extract_album_id(data):
    album_infos = []
    for elem in data['albums']['items']:
        temp = {
            'id': elem['id'],
            'name': elem['name'],
            'release_date': elem['release_date']
        }
        album_infos.append(temp)

    return album_infos

# print(extract_album_id(search_(album='stick season')))

