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

        self.AsyncSessionLocal = async_sessionmaker(self.engine, expire_on_commit=False)
        
    async def get_session(self):
        # 3. Метод зависимости теперь использует публичную фабрику
        # Проверка на всякий случай, если класс еще не был инициализирован
        if self.AsyncSessionLocal is None:
            raise Exception("База данных не инициализирована.")
        async with self.AsyncSessionLocal() as session:
            yield session

db_engine = async_engine_sql()
SessionDep = Annotated[AsyncSession, Depends(db_engine.get_session)]
