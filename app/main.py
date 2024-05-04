# from fastapi import FastAPI
# from api.music import music
# from api.db import metadata, database, engine
#
# metadata.create_all(engine)
#
# app = FastAPI()
#
# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#
# app.include_router(music)


from typing import Union

from fastapi import FastAPI
import api.db


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}