from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()                   

class Settings(BaseModel):
    DATABASE_URL: str = Field(default=os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/workouts"))
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "dev-secret"))
    ACCESS_MIN: int = Field(default=int(os.getenv("ACCESS_MIN", "60")))

settings = Settings()
