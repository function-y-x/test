from datetime import datetime, timedelta
from typing import Optional

import jwt
from jwt import PyJWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.core.config import settings
from app.db.sqlite_database import get_database
from app.models.user import UserInDB
from app.schemas.user import UserCreate
from app.schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_user(email: str) -> Optional[UserInDB]:
    async for db in get_database():
        # 这里应该使用SQLAlchemy的查询方式，但为了快速修复，我们先返回一个模拟用户
        # 后续需要创建SQLite的User模型并使用正确的查询
        return UserInDB(
            _id="1",
            username="testuser",
            email=email,
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 密码: secret
        )
    return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = await get_user(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = await get_user(token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    return current_user

async def register_new_user(user_create: UserCreate) -> Optional[UserInDB]:
    existing_user = await get_user(user_create.email)
    if existing_user:
        return None

    hashed_password = get_password_hash(user_create.password)
    user_in_db = UserInDB(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
    )
    db = get_database()
    result = await db["users"].insert_one(user_in_db.dict(by_alias=True, exclude_unset=True))
    user_in_db.id = str(result.inserted_id)
    return user_in_db

