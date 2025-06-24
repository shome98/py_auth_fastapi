# from fastapi import FastAPI
# from app.routes import router
# from app.db_connect import engine, Base

# # Create the database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Include the API routes
# app.include_router(router)

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the FastAPI User Authentication API"}

# app/main.py

from fastapi import FastAPI
from app.routes import router
from app.db_connect import Base, engine  # Corrected typo
import asyncio
from sqlalchemy import text
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Async-safe way to create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI User Authentication API"}