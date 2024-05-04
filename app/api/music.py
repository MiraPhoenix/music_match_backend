from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from api import db_manager
from api.models import MusicIn, MusicOut

musicc = APIRouter()

fake_music_db = [
    {
        'name': 'Warm',
        'album': 'We laughed, no one understood',
        'genres': 'Hyperpop',
        'casts': '17 SEVENTEEN'
    }
]


class music(BaseModel):
    name: str
    album: str
    genres: str
    casts_id: str

@musicc.post('/', response_model=MusicOut, status_code=201)
async def create_movie(payload: MusicIn, music_id=None, is_cast_present=None):
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

        movie_id = await db_manager.add_music(payload)
        response = {
            'id': music_id,
            **payload.dict()
        }

        return response


@musicc.get('/', response_model=List[MusicOut])
async def index():
    return await db_manager.get_all_music()


@musicc.put('/{id}')
async def update_music(id: int, payload: MusicIn):
    music = payload.dict()
    fake_music_db[id] = music
    return None


@musicc.put('/{id}')
async def update_music(id: int, payload: MusicIn):
    music = await db_manager.get_music(id)
    if not music:
        raise HTTPException(status_code=404, detail="Track not found")


def HTTPException(status_code, detail):
    pass


@musicc.delete('/{id}')
async def delete_music(id: int):
    music = await db_manager.get_music(id)
    if not music:
        raise HTTPException(status_code=404, detail="Track not found")
    return await db_manager.delete_music(id)
