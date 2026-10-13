from backend.db_request import DatabaseClient
from fastapi import APIRouter
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

    with DatabaseClient("AlbumReviews") as db:
        artist_inner_id = db.execute_insert(
        req_add_artist,
        (artist.name, artist.spotify_id)
    )

    return artist_inner_id

@router.get("/{artist_spotify_id}")
def get_artist_by_spotify_id(artist_spotify_id: str):
    req_get_artist = '''
        SELECT id
        FROM artists
        WHERE spotify_id = %s;
    '''

    with DatabaseClient("AlbumReviews") as db:
        result = db.make_request(
        req_get_artist,
        (artist_spotify_id,)
    )

    if result:
        return result[0]['id']

    return None
