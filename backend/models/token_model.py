from pydantic import BaseModel


class PairTokenModel(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenModel(BaseModel):
    access_token: str


class RefreshTokenModel(BaseModel):
    refresh_token: str
