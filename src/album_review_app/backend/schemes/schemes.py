from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=20,
        pattern=r'^[A-Za-z][A-Za-z0-9_]*$'
    )
    email: EmailStr
    password_hash: str = Field(min_length=8)


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class SpotifyArtist(BaseModel):
    spotify_id: str
    name: str

class SpotifyAlbum(BaseModel):
    spotify_id: str
    name: str
    release_date: str
    cover_url: str
    artist: SpotifyArtist