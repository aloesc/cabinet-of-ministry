from sqlalchemy import select
import fastapi
from database.engine import SessionDep
from database.models import Users

async def validate_admin(current_user, session):
    stmt = select(Users).where(Users.username == current_user)
    execution = await session.execute(stmt)
    user = execution.scalar_one_or_none()
    
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    if user.role == "guest":
        raise fastapi.HTTPException(status_code=403, detail="Forbidden")
    
    return user
    
async def validate_user(current_user, session):
    stmt = select(Users).where(Users.username == current_user)
    execution = await session.execute(stmt)
    user = execution.scalar_one_or_none()
    
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    
    return user

async def validate_superuser(current_user, session):
    stmt = select(Users).where(Users.username == current_user)
    execution = await session.execute(stmt)
    user = execution.scalar_one_or_none()
    
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    if user.is_superuser != True:
        raise fastapi.HTTPException(status_code=403, detail="Forbidden")
    
    return user