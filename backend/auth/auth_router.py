from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy import select
from database.engine import SessionDep
from auth.jwt_handler import create_access_token, verify_password, get_password_hash
import database.models as models, schemas

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