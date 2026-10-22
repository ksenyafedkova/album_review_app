import requests
from fastapi import params

from backend.schemes.schemes import UserCreate, SpotifyAlbum, SpotifyArtist

api_url = 'http://127.0.0.1:8000/api/v1'
TIMEOUT = 10

def _send_request(method: str, url: str, **kwargs):
    """Отправляет HTTP-запрос и обрабатывает ошибки."""
    response = requests.request(
        method, url, timeout=TIMEOUT, **kwargs
    )
    response.raise_for_status()
    if not response.content:
        return None

    return response.json()

def get_users():
    url = f"{api_url}/users/"

    return _send_request(
        "GET", url)

def check_user(username_or_email: str):
    url = f"{api_url}/users/check"

    return _send_request(
        "GET",
        url,
        params={"username_or_email": username_or_email}
    )

def create_user(user: UserCreate):
    url = f"{api_url}/users/"

    return _send_request(
        "POST",
        url,
        json=user.model_dump(mode="json")
    )

def get_user_albums(user_id: int):
    url = f"{api_url}/users/{user_id}/albums"

    return _send_request("GET", url)

def add_to_shelf(user_id: int, album_id: int):
    url = f"{api_url}/users/{user_id}/albums/{album_id}"

    return _send_request("POST", url)

def save_album_to_shelf(user_id: int, album: SpotifyAlbum):
    url = f"{api_url}/users/{user_id}/shelf"

    return _send_request(
        "POST", url, json=album.model_dump(mode="json")
    )

def delete_from_shelf(user_id: int, album_id: int):
    url = f"{api_url}/users/{user_id}/albums/{album_id}"

    return _send_request("DELETE", url)


def get_album_by_spotify_id(album_spotify_id: str):
    url = f"{api_url}/albums/{album_spotify_id}"

    return _send_request("GET", url)


def add_album(artist_inner_id: int, album: SpotifyAlbum):
    url = f"{api_url}/albums/"

    return _send_request(
        "POST",
        url,
        params={"artist_inner_id": artist_inner_id},
        json=album.model_dump(mode="json")
    )


def get_artist_by_spotify_id(artist_spotify_id: str):
    url = f"{api_url}/artists/{artist_spotify_id}"

    return _send_request("GET", url)


def add_artist(artist: SpotifyArtist):
    url = f"{api_url}/artists"

    return _send_request(
        "POST",
        url,
        json=artist.model_dump(mode="json")
    )
