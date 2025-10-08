import fastapi
from starlette.responses import StreamingResponse
import schemas
from database.models import Events
from database.engine import SessionDep
from sqlalchemy import select
from auth.jwt_handler import get_current_user
from fastapi import Depends, HTTPException, UploadFile
from services.validate_user import validate_user, validate_admin

router = fastapi.APIRouter(
    prefix="/events",
    tags=["Events"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_events(session: SessionDep, current_user: str = Depends(get_current_user)):
    user = await validate_user(current_user, session)
    stmt = select(Events)
    result = await session.execute(stmt)
    events = result.scalars().all()
    return events

@router.get("/{event_id}")
async def get_event(event_id: int, session: SessionDep, current_user: str = Depends(get_current_user)):
    user = await validate_user(current_user, session)
    stmt = select(Events).where(Events.id == event_id)
    execution = await session.execute(stmt)
    event = execution.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/")
async def create_event(event: schemas.EventCreate, session: SessionDep, current_user: str = Depends(get_current_user)):
    user = await validate_admin(current_user, session)
    new_event = Events(
        title=event.title,
        type_of_event=event.type_of_event,
        description=event.description,
        date_of_event=event.date_of_event,
        location=event.location
    )
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)
    return new_event

