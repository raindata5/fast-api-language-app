# set up the model
# set up the db connection
# connect the db to my app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "mssql+pymssql://raindata5:natalia@localhost/flask_notifications"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = f"mssql+pymssql://{settings.db_user_languages}:{settings.db_pass_languages}@{settings.db_host_languages}/{settings.db_name_languages}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user_languages}:{settings.db_pass_languages}@{settings.db_host_languages}/{settings.DB_NAME}"
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
