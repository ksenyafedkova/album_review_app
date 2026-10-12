from backend.db_request import make_request, execute_request, execute_insert
from fastapi import APIRouter
from pydantic import BaseModel

from backend.v1.albums import get_album_by_spotify_id, add_album
from backend.v1.artists import get_artist_by_spotify_id, add_artist

router = APIRouter(prefix='/users', tags=['users'])

class User(BaseModel):
    username: str
    email: str
    password_hash: str

class SpotifyArtist(BaseModel):
    spotify_id: str
    name: str

class SpotifyAlbum(BaseModel):
    spotify_id: str
    name: str
    release_date: str
    cover_url: str
    artist: SpotifyArtist

@router.get("/")
def get_users():
    query = '''
    SELECT * FROM users
    '''
    users = make_request(query, "AlbumReviews")
    return users

@router.get("/check")
def check_user(username_or_email: str):
    req = 'SELECT * FROM users WHERE username = %s OR email = %s'

    res = make_request(
        req,
        "AlbumReviews",
        (username_or_email, username_or_email))

    return res

@router.post("/")
def create_user(user: User):
    req = 'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)'

    execute_request(
        req,
        'AlbumReviews',
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
    res = make_request(
        req,
        "AlbumReviews",
        (user_id,)
    )

    return res

@router.post("/{user_id}/albums/{album_id}")
def add_to_shelf(user_id: int, album_id: int):
    req_check = '''
            SELECT 1
            FROM users_albums
            WHERE user_id = %s
            AND album_id = %s;
        '''

    result = make_request(
        req_check,
        "AlbumReviews",
        (user_id, album_id)
    )

    if result:
        return False

    req_add_to_shelf = '''
        INSERT INTO users_albums (user_id, album_id)
        VALUES (%s, %s);
    '''

    execute_request(
        req_add_to_shelf,
        "AlbumReviews",
        (user_id, album_id)
    )
    return True

@router.post("/{user_id}/shelf")
def save_album_to_shelf(user_id: int, album: SpotifyAlbum):
    # 1. Проверяем, есть ли альбом в нашей БД
    album_inner_id = get_album_by_spotify_id(album.spotify_id)

    if album_inner_id:
        # Альбом уже есть в БД — просто добавляем его на полку
        return add_to_shelf(user_id, album_inner_id)

    # 2. Проверяем, есть ли артист в нашей БД
    artist_inner_id = get_artist_by_spotify_id(album.artist.spotify_id)

    # 3. Если артиста нет — создаём его
    if not artist_inner_id:
        artist_inner_id = add_artist(album.artist)

    # 4. Создаём альбом и получаем его внутренний id
    album_inner_id = add_album(
        artist_inner_id,
        album
    )

    # 5. Добавляем альбом на полку пользователя
    return add_to_shelf(user_id, album_inner_id)
    # st.write('6. added to shelf')

@router.delete("/{user_id}/albums/{album_id}")
def delete_from_shelf(user_id: int, album_id: int):
    req_delete_from_shelf = '''
        DELETE FROM users_albums
        WHERE user_id = %s AND album_id = %s;
    '''

    execute_request(
        req_delete_from_shelf,
        "AlbumReviews",
        (user_id, album_id)
    )

    return {"success": True}