from backend.db_request import make_request, execute_request, execute_insert
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/albums', tags=['albums'])

class SpotifyArtist(BaseModel):
    spotify_id: str
    name: str

class SpotifyAlbum(BaseModel):
    spotify_id: str
    name: str
    release_date: str
    cover_url: str
    artist: SpotifyArtist

@router.get("/{album_spotify_id}")
def get_album_by_spotify_id(album_spotify_id: str):
    req_get_album = '''
        SELECT id
        FROM albums
        WHERE spotify_id = %s;
    '''

    result = make_request(
        req_get_album,
        "AlbumReviews",
        (album_spotify_id,)
    )

    if result:
        return result[0]['id']

    return None

@router.post("/")
def add_album(
        artist_inner_id: int,
        album: SpotifyAlbum
):
    req_add_album = '''
        INSERT INTO albums
            (artist_id, name, spotify_id, release_date, cover_url)
        VALUES
            (%s, %s, %s, %s, %s);
    '''

    return execute_insert(
        req_add_album,
        "AlbumReviews",
        (
            artist_inner_id,
            album.name,
            album.spotify_id,
            album.release_date,
            album.cover_url)
    )