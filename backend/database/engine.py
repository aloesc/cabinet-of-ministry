from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from os import getenv
from fastapi import Depends
from typing import Annotated



class async_engine_sql():
    def __init__(self):
        DBHOST = getenv("DBHOST", "localhost")
        DBUSER = getenv("DBUSER", "root")
        DBPASSWORD = getenv("DBPASS", "root")
        DBNAME = getenv("DBNAME", "backend")
        DBPORT = getenv("DBPORT", "3306")

        

        DB_URL = f"mysql+aiomysql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

        self.engine = create_async_engine(DB_URL, future=True)

    async def get_session(self):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            yield session



SessionDep = Annotated[AsyncSession, Depends(async_engine_sql().get_session)]
