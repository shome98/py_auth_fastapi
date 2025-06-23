import os
from dotenv import load_dotenv

load_dotenv('.env')

class Settings:
    JWT_SECRET: str=os.getenv("JWT_SECRET")
    ALGORTHM: str="HS256"
    ACEESS_TOKEN_EXPIRE_MINUTES: int=30
    DATABASE_URL :str=os.getenv("POSTGRES_URL")
    if DATABASE_URL is None:
        raise ValueError("Please provide a valid database url 😒")
    if JWT_SECRET is None:
        raise ValueError("Please provide a valid jwt secret 😒")

settings=Settings()
print(settings.DATABASE_URL)