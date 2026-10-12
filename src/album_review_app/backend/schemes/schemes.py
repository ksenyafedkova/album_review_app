from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(min_length=5, max_length=20, pattern='^[A-z][A-z0-9]+')
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