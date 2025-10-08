# create_superuser.py
import os
from database.engine import SessionDep
from auth.jwt_handler import get_password_hash
import database.models as models
from sqlalchemy import select
import asyncio
from database.engine import async_session_local

async def main():
    

    async with async_session_local() as session:  # создаём сессию
        try:
            username = os.getenv("ADMIN_USER", "admin")
            password = os.getenv("ADMIN_PASS", "admin")

            stmt = select(models.Users).where(models.Users.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                hashed = get_password_hash(password)
                superuser = models.Users(
                    username=username,
                    password=hashed,
                    full_name="Superuser",
                    email="admin@example.com",
                    role="admin",
                    is_superuser=True
                )
                session.add(superuser)
                await session.commit()
                print(f"✅ Superuser '{username}' создан.")
            else:
                print(f"ℹ️ Superuser '{username}' уже существует.")
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(main())