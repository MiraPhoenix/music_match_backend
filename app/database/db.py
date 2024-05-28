from typing import Optional

import database.define as db
import sqlalchemy
from sqlalchemy.orm import Session


class User:
    id: int
    username: str
    email: str
    password: str
    avatar: str

    def __init__(self, id, username, email, password, avatar):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar

class Music:
    id: int
    title: str
    artist: str
    album: Optional[str] = None

class Review:
    rating: int
    user_id: int
    music_id: int
    comment: str

    def __init__(self, rating, user_id, music_id, comment):
        self.rating = rating
        self.user_id = user_id
        self.music_id = music_id
        self.comment = comment


def create_user(login, email, password):
    with Session(db.engine) as session:
        session.execute(db.users.insert().values(username=login, email=email, password=password))
        session.commit()

def create_review(rev: Review):
    with Session(db.engine) as session:
        session.execute(db.reviews.insert().values(reviewed_by_id=rev.user_id, song_id=rev.music_id, review=rev.comment, mark=rev.rating))
        session.commit()

def get_user_by_email_or_login(login: str):
    session = Session(db.engine)
    row = session.execute(sqlalchemy.select(db.users).where(sqlalchemy.or_(db.users.columns.username == login, db.users.columns.email == login))).one()
    return User(row[0], row[1], row[2], row[3], row[4])

def get_user_by_id(user_id: int):
    with Session(db.engine) as session:
        try:
            row = session.execute(sqlalchemy.select(db.users).where(db.users.c.id == user_id)).one()
            return User(row[0], row[1], row[2], row[3], row[4])
        except sqlalchemy.exc.NoResultFound:
            return None

def get_music_by_id(music_id: int):
    with Session(db.engine) as session:
        try:
            row = session.execute(sqlalchemy.select(db.musics).where(db.musics.c.id == music_id)).one()
            return Music(row[0], row[1], row[2], row[3])
        except sqlalchemy.exc.NoResultFound:
            return None

def search_music(query: str):
    with Session(db.engine) as session:
        try:
            rows = sqlalchemy.select(db.musics).where(db.musics.c.title.ilike(f'%{query}%')).all()
            return [Music(row[0], row[1], row[2], row[3]) for row in rows]
        except sqlalchemy.exc.NoResultFound:
            return None

def get_reviews_by_user_id(user_id: str):
    with Session(db.engine) as session:
        try:
            rows = session.execute(sqlalchemy(db.reviews).where(db.reviews.c.user_id == user_id)).all()
            return [Review(row[0], row[1], row[2], row[3]) for row in rows]
        except sqlalchemy.exc.NoResultFound:
            return None

def get_reviews_by_music_id(music_id: str):
    with Session(db.engine) as session:
        try:
            rows = session.execute(sqlalchemy(db.reviews).where(db.reviews.c.user_id == music_id)).all()
            return [Review(row[0], row[1], row[2], row[3]) for row in rows]
        except sqlalchemy.exc.NoResultFound:
            return None