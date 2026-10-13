from fastapi import FastAPI

from album_review_app.backend.v1.router import api_router

def create_app():
    app = FastAPI(title='Album Apps', version='0.1.0')
    app.include_router(api_router, prefix='/api/v1')

    return app

app = create_app()

