from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class RegisterUserRequest(BaseModel):
    login: str
    email: str
    password: str


@router.post('/user/register')
def register_user(req: RegisterUserRequest):
    return {"Hello": "World"}


class LoginUserRequest(BaseModel):
    login: str
    password: str


class LoginUserResponse(BaseModel):
    token: str


@router.post('/user/login')
def login_user(req: LoginUserRequest):
    return LoginUserResponse(token='test')


class UpdateUserRequest(BaseModel):
    login: str
    email: str
    avatar: str


@router.put('/user')
def update_user(req: UpdateUserRequest):
    return {}


class GetUserResponse(BaseModel):
    login: str
    email: str
    avatar: str
    reviews_count: int
    avg_mark: float


@router.get('/user')
def get_user(id: int):
    return GetUserResponse()

@router.get('/user/reviews')
def get_user_reviews(id: int):
    return List[Review]


class Music(BaseModel):
    id: int
    name: str
    singer: str
    icon: str
    data: str


@router.get('/musics')
def get_musics():
    return List[Music]

@router.get('/music')
def get_music(id: int):
    return Music()

@router.get('/music/search')
def search_music(text: str):
    return List[Music]


class CreateReviewRequest(BaseModel):
    id: int
    text: str
    mark: int


@router.post('/music/review')
def create_review(req: CreateReviewRequest):
    return {}

class Review(BaseModel):
    id: int
    reviewer_id: int
    text: str
    mark: int


@router.get('/music/review')
def get_reviews(id: int):
    return List[Review]