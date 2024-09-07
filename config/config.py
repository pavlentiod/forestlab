import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# load_dotenv()
BASE_DIR = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env-dev")


class DbSettings(BaseModel):
    username: str = os.getenv("DATABASE_USER")
    password: str = os.getenv("DATABASE_PASSWORD")
    host: str = os.getenv("DATABASE_HOST")
    name: str = os.getenv("DATABASE_NAME")
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}/{self.name}"


class Settings(BaseSettings):
    db: DbSettings = DbSettings()


settings = Settings()
