from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from datetime import timedelta, datetime
from sqlalchemy import select
from database.engine import SessionDep
from auth.jwt_handler import create_access_token, verify_password, get_password_hash
import database.models as models, schemas
import secrets
from datetime import datetime, timedelta
from services.send_mail import send_email
from database.models import Users
import requests

import secrets
import string

def generate_password(length: int = 12) -> str:
    # Символы для пароля
    characters = string.ascii_letters + string.digits + string.punctuation
    # Генерация пароля
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(user: schemas.UserLogin, session: SessionDep):
    stmt = select(models.Users).where(models.Users.username == user.username)
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: schemas.UserCreate, session: SessionDep):
    hashed_password = get_password_hash(user.password)
    new_user = models.Users(username=user.username,
                            password=hashed_password,
                            email=user.email,
                            full_name=user.full_name or None,
                            phonenumber=user.phonenumber or None,
                            date_of_birth=user.date_of_birth or None,
                            gender=user.gender)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/forgot_password")
async def forgot_password(user: schemas.UserForgotPassword, background_tasks: BackgroundTasks, session: SessionDep):
    result = await session.execute(select(Users).where(Users.email == user.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=30)
    
    user.reset_token = token
    user.reset_token_expires = expires
    session.add(user)
    await session.commit()

    # 4. Отправляем письмо в фоне
    ip = requests.get('https://api.ipify.org').text
    reset_link = f"https://{ip}:8000/auth/reset_password?token={token}"
    background_tasks.add_task(send_email, to=user.email, subject="Password reset", body=f"Сброс пароля: {reset_link}")

@router.get("/reset_password")
async def reset_password(session: SessionDep, background_tasks: BackgroundTasks, token: str = Query(...)):
    result = await session.execute(select(Users).where(Users.reset_token == token))
    user_obj = result.scalar_one_or_none()
    if not user_obj or datetime.fromisoformat(user_obj.reset_token_expires) < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    password = generate_password()
    
    background_tasks.add_task(send_email, to=user_obj.email, subject="Password reset", body=f"Новый пароль {password}")
    hashed_password = get_password_hash(password)
    user_obj.password = hashed_password
    user_obj.reset_token = None
    user_obj.reset_token_expires = None
    session.add(user_obj)
    await session.commit()
    return {"message": "Пароль был отправлен на почту"}