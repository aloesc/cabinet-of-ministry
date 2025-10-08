from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import routers.documents as documents
import auth.auth_router as auth
import routers.users as users
import routers.events as events

from database.engine import SessionDep
from auth.jwt_handler import get_password_hash
import database.models as models
from sqlalchemy import select
import os
from contextlib import asynccontextmanager

app = FastAPI()


app.include_router(documents.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(events.router)
#app.include_router(bill.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)