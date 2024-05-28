from typing import List, Annotated, Union

from fastapi import APIRouter, HTTPException, Header, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import database.db as db
import bcrypt
import jwt

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwtSecret = "jI1i*2ndIU2j3"

router = APIRouter()


class RegisterUserRequest(BaseModel):
    login: str
    email: str
    password: str


@router.post('/user/register')
async def register_user(req: RegisterUserRequest):
    try:
        hash_password = bcrypt.hashpw(
            password=req.password.encode('utf-8'),
            salt=bcrypt.gensalt()
        )

        db.create_user(req.login, req.email, hash_password.decode('utf8'))
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to create user: " + str(error))


class LoginUserRequest(BaseModel):
    login: str
    password: str


class LoginUserResponse(BaseModel):
    token: str


@router.post('/user/login')
async def login_user(req: LoginUserRequest):
    # return db.get_user_by_email_or_login(loginn)
    # return req
    try:
        user = db.get_user_by_email_or_login(req.login)
        if not bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8')):
            return HTTPException(status_code=400, detail="Password not equals")

        token = jwt.encode(payload={"id": user.id}, key=jwtSecret, algorithm="HS256")

        return LoginUserResponse(token=token)
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to get user: " + str(error))


class UpdateUserRequest(BaseModel):
    login: str
    email: str
    avatar: str


@router.put('/user')
async def update_user(req: UpdateUserRequest):
    if id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    user = db[id]
    user.update(req.dict())
    return {"message": "User updated successfully"}


class GetUserResponse(BaseModel):
    login: str
    email: str
    avatar: str
    reviews_count: int
    avg_mark: float


@router.get('/user')
async def get_user(id: str):
    try:

        # if id not in db:
        #     raise HTTPException(status_code=404, detail="User not found")
        user = db.get_user_by_id(id)
        return user
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to get user: " + str(error))
    # print('1')
    # user = db[id]
    # print('2')
    # reviews = db.get(id, [])
    # print('3')
    # all_marks = sum(review['mark'] for review in reviews) / len(reviews) if reviews else 0
    # print('4')
    return user


class Review(BaseModel):
    id: str
    user_id: int
    music_id: int
    mark: int
    text: str


@router.get('/user/reviews/{user_id}')
async def get_user_reviews(id: str):
    try:
        reviews = db.get_reviews_by_user_id(id)
        return reviews
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to get user reviews: " + str(error))


class Music(BaseModel):
    id: int
    name: str
    singer: str
    icon: str
    data: str


@router.get('/musics')
async def get_musics():
    try:
        musics = db.get_all_musics()
        return musics
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to get musics: " + str(error))


@router.get('/music/{id}')
async def get_music(id: str):
    try:
        music = db.get_music_by_id(id)
        return music
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to get music: " + str(error))


@router.get('/music/search')
async def search_music(query: str):
    try:
        results = search_music(query)
        return results
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to search music: " + str(error))


class CreateReviewRequest(BaseModel):
    id: int
    text: str
    mark: int
    music_id: int



# class Review(BaseModel):
#     user_id: int
#     music_id: int
#     text: str
#     mark: int


@router.post('/music/review')
async def create_review(req: CreateReviewRequest):
    try:
        new_review = db.Review(
            user_id=req.id,
            music_id=req.music_id,
            rating=req.mark,
            comment=req.text
        )
        db.create_review(new_review)
        return {"message": "Review created successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to create review: " + str(error))


@router.get('/music/review')
async def get_reviews(music_id: str):
    try:
        reviews = db.get_reviews_by_music_id(music_id)
        return reviews
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to get music review: " + str(error))
