# import asyncio
# from sqlalchemy import text
# from dotenv import load_dotenv
# from urllib.parse import urlparse
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # from .config import settings


# import os
# from dotenv import load_dotenv

# load_dotenv('.env')


# DATABASE_URL :str=os.getenv("POSTGRES_URL")
# # tmpPostgres = urlparse(settings.DATABASE_URL)
# tmpPostgres = urlparse(DATABASE_URL)
# engine = create_async_engine(f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=True)
# # engine = create_async_engine(DATABASE_URL, future=True, echo=True)
# SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine,class_=AsyncSession)
# Base=declarative_base()
# async def get_db_session():
#     async with SessionLocal() as session:
#         yield session

# # async def main():
# #     gen = get_db_session()
# #     try:
# #         session = await gen.__anext__()
# #         print("Got session:", session)
# #         # You can now use the session
# #     finally:
# #         await gen.aclose()

# # if __name__ == "__main__":
# #     asyncio.run(main())

# app/db_connect.py

from sqlalchemy import text
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_URL = os.getenv("POSTGRES_URL")
if not DATABASE_URL:
    raise ValueError("Missing POSTGRES_URL in environment")

tmpPostgres = urlparse(DATABASE_URL)

engine = create_async_engine(
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require",
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db_session():
    async with SessionLocal() as session:
        yield session