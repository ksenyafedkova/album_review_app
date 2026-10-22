import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

class SpotifyClient:

    def __init__(self):
        self.token_data = None

    def get_access_token(self):
        # Получаем токен Spotify
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

    def _ensure_token(self):
        # Проверяем, действителен ли токен
        if (
                self.token_data is None
                or datetime.now() >= self.token_data['expires_at']
        ):
            self.token_data = self.get_access_token()

        return self.token_data['access_token']


    def get_full_album_info(self, album_spotify_id):
        # Получаем информацию об альбоме
        url = f'https://api.spotify.com/v1/albums/{album_spotify_id}'

        token = self._ensure_token()

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

    def search(self, album='', artist=''):
        url = 'https://api.spotify.com/v1/search'

        token = self._ensure_token()


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

        else:
            raise ValueError("Write the name of the album")

        headers = {
                'Authorization': f'Bearer {token}'
            }

        response = requests.get(url, headers=headers, params=params)

        data = response.json()
        return data

    def extract_basic_album_info(self, data):
        # Извлекаем нужную информацию из результатов поиска
        album_infos = []
        for elem in data['albums']['items']:
            temp = {
                'id': elem['id'],
                'name': elem['name'],
                'release_date': elem['release_date']
            }
            album_infos.append(temp)

        return album_infos



