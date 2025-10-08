from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from os import getenv
from fastapi import Depends
from typing import Annotated

DBHOST = getenv("DBHOST", "localhost")
DBUSER = getenv("DBUSER", "root")
DBPASSWORD = getenv("DBPASS", "root")
DBNAME = getenv("DBNAME", "backend")
DBPORT = getenv("DBPORT", "3306")

DB_URL = f"mysql+aiomysql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

engine = create_async_engine(DB_URL, future=True)
async_session_local = async_sessionmaker(engine, expire_on_commit=False)

# Для эндпоинтов FastAPI
async def get_session() -> AsyncSession:
    async with async_session_local() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]