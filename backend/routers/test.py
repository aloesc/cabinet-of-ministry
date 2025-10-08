import fastapi
from fastapi import Depends
from starlette.responses import FileResponse
import schemas
from database.models import Documents
from database.engine import SessionDep
from sqlalchemy import select
from auth.jwt_handler import get_current_user

router = fastapi.APIRouter(
    prefix="/test",
    tags=["tests"],
    responses={404: {"description": "Not found"}},
)

@router.get("/secure")
async def secure_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}!"}