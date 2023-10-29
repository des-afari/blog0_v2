from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_DRIVERNAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str

    class Config:
        env_file = '.env'

settings = Settings()