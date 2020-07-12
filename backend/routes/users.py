import os
import jwt

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from pymongo import errors

from ..db import db

router = APIRouter()

users = db.users

users.create_index('username', unique=True)
users.create_index('email', unique=True)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogIn(User):
    email: Optional[EmailStr]
    username: Optional[str]


class UserProfile(User):
    username: str
    email: str
    full_name: Optional[str] = None
    about: Optional[str] = None
    followers: Optional[int] = 0
    following: Optional[int] = 0


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    user = users.find_one({'username': username})
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/register')
async def register_user(user: User):
    user = {
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'password': get_password_hash(user.password)
    }
    try:
        users.insert_one(user)
    except errors.DuplicateKeyError as e:
        if 'email' in e.__str__():
            return Response('that email is taken', status_code=409)
        elif 'username' in e.__str__():
            return Response('that username is taken', status_code=409)
    return {'message': 'user registered'}


@router.post('/login')
async def login_user(user: UserLogIn):
    current_user = get_user(user.username)
    if not current_user or not verify_password(user.password,
                                               current_user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/{user_id}')
async def get_user_profile(user_id: int, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user(username)
    user = UserProfile(**user)
    return user
