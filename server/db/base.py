from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL
from utils.config import settings

Base = declarative_base()

MYSQL_URL = URL.create(
    drivername=settings.DB_DRIVERNAME,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_DATABASE
)

engine = create_engine(MYSQL_URL)
DB_LOCAL = sessionmaker(bind=engine, autoflush=False)