from fastapi import APIRouter

from album_review_app.backend.v1 import users, artists, albums

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(artists.router)
api_router.include_router(albums.router)
