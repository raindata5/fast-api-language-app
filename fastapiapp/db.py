# set up the model
# set up the db connection
# connect the db to my app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import redis
import json

# SQLALCHEMY_DATABASE_URL = "mssql+pymssql://raindata5:natalia@localhost/flask_notifications"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = f"mssql+pymssql://{settings.db_user_languages}:{settings.db_pass_languages}@{settings.db_host_languages}/{settings.db_name_languages}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.postgres_redis}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def start_redis():
    redis_client = redis.Redis(
        host='127.0.0.1',
        port=6379)
    try:
        yield redis_client
    finally:
        None