from backend.db_request import make_request, execute_request, execute_insert
from fastapi import FastAPI
from pydantic import BaseModel

from album_review_app.backend.v1.router import api_router

def create_app():
    app = FastAPI(title='Album Apps', version='0.1.0')
    app.include_router(api_router, prefix='/api/v1')

    return app

app = create_app()



# class User(BaseModel):
#     username: str
#     email: str
#     password_hash: str
#
# class SpotifyArtist(BaseModel):
#     spotify_id: str
#     name: str
#
# class SpotifyAlbum(BaseModel):
#     spotify_id: str
#     name: str
#     release_date: str
#     cover_url: str
#     artist: SpotifyArtist
