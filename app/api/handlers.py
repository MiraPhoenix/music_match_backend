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
async def get_user(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    user = db[id]
    reviews = db.get(id, [])
    all_marks = sum(review['mark'] for review in reviews) / len(reviews) if reviews else 0
    return List[GetUserResponse]

class Review(BaseModel):
    id: int
    user_id: int
    music_id: int
    mark: int
    text: str

@router.get('/user/reviews')
async def get_user_reviews(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return List[Review]


class Music(BaseModel):
    id: int
    name: str
    singer: str
    icon: str
    data: str


@router.get('/musics', response_model=List[Music])
async def get_musics():
    return List[Music]

@router.get('/music', response_model=Music)
async def get_music(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Song is not found")
    return List[Music]

@router.get('/music/search', response_model=List[Music])
async def search_music(text: str):
    if text not in db:
        raise HTTPException(status_code=404, detail="Song is not found")
    return List[Music]


class CreateReviewRequest(BaseModel):
    token: str
    id: int
    text: str
    mark: int


@router.post('/music/review')
async def create_review(req: CreateReviewRequest):
    try:
        new_review = Review(
            user_id=req.user_id,
            music_id=req.music_id,
            rating=req.rating,
            comment=req.comment
        )
        db.session.add(new_review)
        db.session.commit()
        return {"message": "Review created successfully"}
    except Exception as error:
            raise HTTPException(status_code=500, detail="Failed to create review: " + str(error))

class Review(BaseModel):
    id: int
    reviewer_id: int
    text: str
    mark: int


@router.get('/music/review', response_model=List[Review])
async def get_reviews(id: int):
    if id not in db:
        return []
    return List[Review]