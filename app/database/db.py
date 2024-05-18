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


def create_user(login, email, password):
    with Session(db.engine) as session:
        session.execute(db.users.insert().values(username=login, email=email, password=password))
        session.commit()


def get_user_by_email_or_login(login):
    session = Session(db.engine)
    row = session.execute(sqlalchemy.select(db.users).where(sqlalchemy.or_(db.users.columns.username == login, db.users.columns.email == login))).one()
    return User(row[0], row[1], row[2], row[3], row[4])
