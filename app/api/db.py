import sqlalchemy as db


DATABASE_URL = 'postgresql://postgres:test@127.0.0.1:54320/postgres?'

engine = db.create_engine(DATABASE_URL)
conn = engine.connect()
metadata = db.MetaData()

userIDSeq = db.Sequence('user_id_seq')
users = db.Table('users', metadata,
  db.Column('id', db.Integer, userIDSeq, primary_key=True),
  db.Column('username', db.Text),
  db.Column('email', db.Text),
  db.Column('password', db.Text),
  db.Column('avatar', db.Text),
)

musicIDSeq = db.Sequence('music_id_seq')
music = db.Table('music', metadata,
  db.Column('id', db.Integer, musicIDSeq, primary_key=True),
  db.Column('name', db.Text),
  db.Column('singer', db.Text),
  db.Column('icon', db.Text),
  db.Column('data', db.Integer),
)

reviewIDSeq = db.Sequence('review_id_seq')
reviews = db.Table('reviews', metadata,
  db.Column('id', db.Integer, reviewIDSeq, primary_key=True),
  db.Column('reviewed_by_id', db.Integer, db.ForeignKey('users.id')),
  db.Column('song_id', db.Integer, db.ForeignKey('music.id')),
  db.Column('review', db.Text),
  db.Column('mark', db.SmallInteger),
  db.CheckConstraint("mark > 0", name="mark_min"),
  db.CheckConstraint("mark <= 10", name="mark_max")
)

metadata.create_all(engine)

music.insert().values(name = 'test')