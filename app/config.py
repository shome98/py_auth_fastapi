import os
from dotenv import load_dotenv

load_dotenv('.env')

class Settings:
    JWT_SECRET: str = os.getenv("JWT_SECRET", "fallback_secret_key")
    ALGORTHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")

    def __init__(self):
        if self.POSTGRES_URL is None:
            raise ValueError("Please provide a valid database URL 😒")
        if self.JWT_SECRET is None:
            raise ValueError("Please provide a valid JWT secret 😒")


settings = Settings()