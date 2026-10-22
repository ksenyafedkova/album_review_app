from backend.db_request import DatabaseClient
from fastapi import APIRouter

# добавляем функции, которые используют уже открытое подключение к БД:
from backend.v1.albums import find_album_inner_id, add_album_to_db
from backend.v1.artists import find_artist_inner_id, add_artist_to_db
from backend.schemes.schemes import UserCreate, UserLogin, SpotifyAlbum, SpotifyArtist

router = APIRouter(prefix='/users', tags=['users'])

def add_album_to_user_shelf(db, user_id: int, album_id: int):
    req_check = """
        SELECT 1
        FROM users_albums
        WHERE user_id = %s AND album_id = %s;
    """

    result = db.make_request(req_check, (user_id, album_id))

    if result:
        return False

    req_add = """
        INSERT INTO users_albums (user_id, album_id)
        VALUES (%s, %s);
    """

    db.execute_request(req_add, (user_id, album_id))

    return True


@router.get("/")
def get_users():
    query = '''
    SELECT * FROM users
    '''
    with DatabaseClient("AlbumReviews") as db:
        users = db.make_request(query)
    return users

@router.get("/check")
def check_user(username_or_email: str):
    req = 'SELECT * FROM users WHERE username = %s OR email = %s'

    with DatabaseClient("AlbumReviews") as db:
        res = db.make_request(
            req,
            (username_or_email, username_or_email))

    return res

@router.post("/")
def create_user(user: UserCreate):
    req = 'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)'

    with DatabaseClient("AlbumReviews") as db:
        db.execute_request(
            req,
            (user.username, user.email, user.password_hash)
            )
    return {"success": True}

@router.get("/{user_id}/albums")
def get_user_albums(user_id: int):
    req = '''
    SELECT albums.*, artists.name AS artist_name
    FROM albums
    JOIN users_albums
    ON albums.id = users_albums.album_id
    JOIN users
    ON users.id = users_albums.user_id
    JOIN artists
    ON artists.id = albums.artist_id
    WHERE users.id = %s;
'''
    with DatabaseClient("AlbumReviews") as db:
        res = db.make_request(
            req,
            (user_id,)
        )

    return res

@router.post("/{user_id}/albums/{album_id}")
def add_to_shelf(user_id: int, album_id: int):
    with DatabaseClient("AlbumReviews") as db:
        return add_album_to_user_shelf(
            db, user_id, album_id
        )



@router.post("/{user_id}/shelf")
def save_album_to_shelf(user_id: int, album: SpotifyAlbum):

    with DatabaseClient("AlbumReviews") as db:

        # 1. Проверяем, есть ли альбом в нашей БД
        album_inner_id = find_album_inner_id(
            db, album.spotify_id
        )

        # 2. Если альбом уже есть, добавляем его на полку
        if album_inner_id:
            return add_album_to_user_shelf(
                db, user_id, album_inner_id
            )

        # 3. Проверяем, есть ли артист в нашей БД
        artist_inner_id = find_artist_inner_id(
            db, album.artist.spotify_id
        )

        # 4. Если артиста нет, создаём его
        if not artist_inner_id:
            artist_inner_id = add_artist_to_db(
                db, album.artist
            )

        # 5. Создаём альбом
        album_inner_id = add_album_to_db(
            db, artist_inner_id, album
        )

        # 6. Добавляем альбом на полку пользователя
        return add_album_to_user_shelf(
            db, user_id, album_inner_id
        )


@router.delete("/{user_id}/albums/{album_id}")
def delete_from_shelf(user_id: int, album_id: int):
    req_delete_from_shelf = '''
        DELETE FROM users_albums
        WHERE user_id = %s AND album_id = %s;
    '''
    with DatabaseClient("AlbumReviews") as db:
        db.execute_request(
            req_delete_from_shelf,
            (user_id, album_id)
        )

    return {"success": True}