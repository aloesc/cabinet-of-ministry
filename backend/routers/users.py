import fastapi
import schemas
from database.models import Users
from database.engine import SessionDep
from sqlalchemy import select
from auth.jwt_handler import get_password_hash
from auth.validate_user import validate_admin, validate_user
from auth.jwt_handler import get_current_user
from fastapi import Depends

router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"],
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
