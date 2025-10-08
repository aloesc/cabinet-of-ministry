import fastapi
import schemas
from database.models import Users
from database.engine import SessionDep
from sqlalchemy import select
from auth.jwt_handler import get_password_hash
from services.validate_user import validate_admin, validate_user, validate_superuser
from auth.jwt_handler import get_current_user
from fastapi import Depends

router = fastapi.APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_users(session: SessionDep, current_user: str = Depends(get_current_user)):
    user_endpoint = await validate_user(current_user, session)
    stmt = select(Users)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users



@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep, current_user: str = Depends(get_current_user)):
    user_endpoint = await validate_user(current_user, session)
    stmt = select(Users).where(Users.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None or user.role == "guest":
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender
    }

@router.put("/{user_id}")
async def update_user(user_id: int, user: schemas.UserUpdate, session: SessionDep, current_user: str = Depends(get_current_user)):
    user_endpoint = await validate_superuser(current_user, session)
    stmt = select(Users).where(Users.id == user_id)
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    if user.full_name:
        db_user.full_name = user.full_name
    if user.email:
        db_user.email = user.email
    if user.date_of_birth:
        db_user.date_of_birth = user.date_of_birth
    if user.gender:
        db_user.gender = user.gender
    if user.password:
        db_user.password = get_password_hash(user.password)
    if user.role:
        db_user.role = user.role
    if user.is_superuser:
        db_user.is_superuser = user.is_superuser
    
    await session.commit()
    return {
        "id": db_user.id ,
        "full_name": db_user.full_name,
        "email": db_user.email,
        "date_of_birth": db_user.date_of_birth,
        "gender": db_user.gender,
        "role": db_user.role,
        "is_superuser": db_user.is_superuser,
    }
