from backend.db_request import DatabaseClient
from fastapi import APIRouter
from backend.schemes.schemes import SpotifyAlbum

router = APIRouter(prefix="/albums", tags=["albums"])


def find_album_inner_id(db, album_spotify_id: str):
    query = """
        SELECT id
        FROM albums
        WHERE spotify_id = %s;
    """

    result = db.make_request(query, (album_spotify_id,))

    if result:
        return result[0]["id"]

    return None


@router.get("/{album_spotify_id}")
def get_album_by_spotify_id(album_spotify_id: str):
    with DatabaseClient("AlbumReviews") as db:
        return find_album_inner_id(db, album_spotify_id)


def add_album_to_db(db, artist_inner_id: int, album: SpotifyAlbum):
    query = """
        INSERT INTO albums
            (artist_id, name, spotify_id, release_date, release_date_precision, cover_url)
        VALUES
            (%s, %s, %s, %s, %s, %s);
    """

    return db.execute_insert(
        query,
        (
            artist_inner_id,
            album.name,
            album.spotify_id,
            album.release_date,
            album.release_date_precision,
            album.cover_url
        )
    )


@router.post("/")
def add_album(artist_inner_id: int, album: SpotifyAlbum):
    with DatabaseClient("AlbumReviews") as db:
        return add_album_to_db(db, artist_inner_id, album)
