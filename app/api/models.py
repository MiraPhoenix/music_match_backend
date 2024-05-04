from typing import Optional
from pydantic import BaseModel

class music(BaseModel):
    name: str
    album: str
    genres: str
    casts_id: int


class MusicIn(BaseModel):
    pass


class MusicOut(MusicIn):
    id: int


class MusicUpdate(MusicIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[str] = None
    casts_id: Optional[int] = None

