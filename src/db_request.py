import os
from urllib.parse import uses_relative

from dotenv import load_dotenv
import mysql.connector
from logger import logger
import streamlit as st


load_dotenv()

def _get_connection(database=None):
    kwargs = {
        "host": os.getenv('DB_HOST'),
        "user": os.getenv('DB_USER')
    }

    if database:
        kwargs['database'] = database

    return mysql.connector.connect(**kwargs)

def make_request(req, db_name, args=tuple()):
    connection = None
    cursor = None

    try:
        connection = _get_connection(db_name)
        cursor = connection.cursor(dictionary=True)

        if args:
            cursor.execute(req, args)
        else:
            cursor.execute(req)

        res = cursor.fetchall()
        return res

    except Exception as e:
        logger.error(f'Database request failed: {e}')
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def execute_request(req, db_name, args=()):
    connection = None
    cursor = None

    try:
        connection = _get_connection(db_name)
        cursor = connection.cursor()

        if args:
            cursor.execute(req, args)
        else:
            cursor.execute(req)

        connection.commit()

    except Exception as e:
        logger.error(f'Database request failed: {e}')
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def execute_insert(req, db_name, args=()):
    connection = None
    cursor = None

    try:
        connection = _get_connection(db_name)
        cursor = connection.cursor()

        if args:
            cursor.execute(req, args)
        else:
            cursor.execute(req)

        connection.commit()
        return cursor.lastrowid

    except Exception as e:
        logger.error(f'Database request failed: {e}')
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def check_user(username_or_email):
    req = 'SELECT * FROM users WHERE username = %s OR email = %s'

    res = make_request(
        req,
        "AlbumReviews",
        (username_or_email, username_or_email))

    return res

def create_user(username, email, password_hash):
    req = 'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)'

    execute_request(
        req,
        'AlbumReviews',
        (username, email, password_hash)
                    )

def get_user_albums(username):
    req = '''
    SELECT albums.*, artists.name AS artist_name
    FROM albums
    JOIN users_albums
    ON albums.id = users_albums.album_id
    JOIN users
    ON users.id = users_albums.user_id
    JOIN artists
    ON artists.id = albums.artist_id
    WHERE users.username = %s;
'''
    res = make_request(
        req,
        "AlbumReviews",
        (username,)
    )

    return res

def add_artist(name, spotify_id):
    req_add_artist = '''
        INSERT INTO artists (name, spotify_id)
        VALUES (%s, %s);
    '''

    return execute_insert(
        req_add_artist,
        "AlbumReviews",
        (name, spotify_id)
    )

def get_artist(spotify_id):
    req_get_artist = '''
        SELECT id
        FROM artists
        WHERE spotify_id = %s;
    '''

    result = make_request(
        req_get_artist,
        "AlbumReviews",
        (spotify_id,)
    )

    if result:
        return result[0]['id']

    return None

def get_album(spotify_id):
    req_get_album = '''
        SELECT id
        FROM albums
        WHERE spotify_id = %s;
    '''

    result = make_request(
        req_get_album,
        "AlbumReviews",
        (spotify_id,)
    )

    if result:
        return result[0]['id']

    return None

def add_album(artist_id, name, spotify_id, release_date, cover_url):
    req_add_album = '''
        INSERT INTO albums
            (artist_id, name, spotify_id, release_date, cover_url)
        VALUES
            (%s, %s, %s, %s, %s);
    '''

    return execute_insert(
        req_add_album,
        "AlbumReviews",
        (artist_id, name, spotify_id, release_date, cover_url)
    )

def add_to_shelf(user_id, album_id):
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

def save_album_to_shelf(user_id, album):
    # 1. Проверяем, есть ли альбом в нашей БД
    album_id = get_album(album['id'])
    # st.write('1. album_id:', album_id)

    if album_id:
        # Альбом уже есть в БД — нам больше ничего создавать не нужно
        return add_to_shelf(user_id, album_id)
        # st.write('2. added existing album')


    # 2. Проверяем, есть ли артист в нашей БД
    artist = album['artists'][0]
    artist_id = get_artist(artist['id'])
    # st.write('3. artist_id:', artist_id)

    # 3. Если артиста нет — создаём его
    if not artist_id:
        artist_id = add_artist(
            artist['name'],
            artist['id']
        )
        # st.write('4. new artist_id:', artist_id)

    # 4. Создаём альбом и получаем его внутренний id
    album_id = add_album(
        artist_id,
        album['name'],
        album['id'],
        album['release_date'],
        album['images'][0]['url']
    )
    # st.write('5. new album_id:', album_id)

    # 5. Добавляем альбом на полку пользователя
    return add_to_shelf(user_id, album_id)
    # st.write('6. added to shelf')

def delete_from_shelf(user_id, album_id):
    req_delete_from_shelf = '''
        DELETE FROM users_albums
        WHERE user_id = %s AND album_id = %s;
    '''

    execute_request(
        req_delete_from_shelf,
        "AlbumReviews",
        (user_id, album_id)
    )


