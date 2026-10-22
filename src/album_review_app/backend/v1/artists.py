from backend.db_request import DatabaseClient
from fastapi import APIRouter
from backend.schemes.schemes import SpotifyArtist

router = APIRouter(prefix="/artists", tags=["artists"])


def find_artist_inner_id(db, artist_spotify_id: str):
    query = """
        SELECT id
        FROM artists
        WHERE spotify_id = %s;
    """

    result = db.make_request(query, (artist_spotify_id,))

    if result:
        return result[0]["id"]

    return None


@router.get("/{artist_spotify_id}")
def get_artist_by_spotify_id(artist_spotify_id: str):
    with DatabaseClient("AlbumReviews") as db:
        return find_artist_inner_id(db, artist_spotify_id)


def add_artist_to_db(db, artist: SpotifyArtist):
    query = """
        INSERT INTO artists (name, spotify_id)
        VALUES (%s, %s);
    """

    return db.execute_insert(
        query,
        (artist.name, artist.spotify_id)
    )


@router.post("")
def add_artist(artist: SpotifyArtist):
    with DatabaseClient("AlbumReviews") as db:
        return add_artist_to_db(db, artist)
