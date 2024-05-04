from api.db import music, database
from api.models import MusicIn, music


async def add_music(payload: MusicIn):
    query = music.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_music():
    query = music.select()
    return await database.fetch_all(query=query)

async def get_music(id):
    query = music.select(music.c.id==id)
    return await database.fetch_one(query=query)

async def delete_music(id: int):
    query = music.delete().where(music.c.id==id)
    return await database.execute(query=query)

async def update_music(id: int, payload: MusicIn):
    query = (
        music
        .update()
        .where(music.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)