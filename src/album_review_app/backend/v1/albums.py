from backend.db_request import DatabaseClient
from fastapi import APIRouter
from backend.schemes.schemes import SpotifyAlbum, SpotifyArtist

router = APIRouter(prefix='/albums', tags=['albums'])

@router.get("/{album_spotify_id}")
def get_album_by_spotify_id(album_spotify_id: str):
    req_get_album = '''
        SELECT id
        FROM albums
        WHERE spotify_id = %s;
    '''

    with DatabaseClient("AlbumReviews") as db:
        result = db.make_request(
            req_get_album,
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

    with DatabaseClient("AlbumReviews") as db:
        album_inner_id = db.execute_insert(
            req_add_album,
            (
                artist_inner_id,
                album.name,
                album.spotify_id,
                album.release_date,
                album.cover_url
            )
        )

    return album_inner_id