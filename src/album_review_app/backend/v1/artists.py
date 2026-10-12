from backend.db_request import make_request, execute_request, execute_insert
from fastapi import APIRouter
from pydantic import BaseModel
from backend.schemes.schemes import SpotifyArtist

router = APIRouter(prefix='/artists', tags=['artists'])



@router.post("")
def add_artist(
        artist: SpotifyArtist
):
    req_add_artist = '''
        INSERT INTO artists (name, spotify_id)
        VALUES (%s, %s);
    '''

    return execute_insert(
        req_add_artist,
        "AlbumReviews",
        (artist.name, artist.spotify_id)
    )

@router.get("/{artist_spotify_id}")
def get_artist_by_spotify_id(artist_spotify_id: str):
    req_get_artist = '''
        SELECT id
        FROM artists
        WHERE spotify_id = %s;
    '''

    result = make_request(
        req_get_artist,
        "AlbumReviews",
        (artist_spotify_id,)
    )

    if result:
        return result[0]['id']

    return None
