from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapiapp.config import settings
import redis
from fastapiapp.db import get_db, Base, start_redis
from alembic.config import Config
from alembic import command
import pytest
import datetime
from fastapi.testclient import TestClient
from pydantic.networks import EmailStr
from fastapiapp.main import app

from fastapi import status, HTTPException
from fastapiapp import oauth2
from jose import jwt
from fastapiapp.oauth2 import create_access_token
from fastapiapp import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.postgres_redis}-test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal_test_db = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# @pytest.fixture


@pytest.fixture
def session_db():
    # if I leave alembic in these fixtures then these cmds run multiple times
    # it must be placed directly in test python file where these functions are imported
    # or placed outside them
    # unless I change the scope ^_^
    alembic_cfg = Config("\\Users\\Ron\\git-repos\\fast-api-languages-orig\\alembic.ini")
    alembic_cfg.set_main_option('script_location', "\\Users\\Ron\\git-repos\\fast-api-languages-orig\\alembic_languages_db")
    alembic_cfg.set_main_option("sqlalchemy.url", f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.postgres_redis}-test")
    print(alembic_cfg.get_main_option("sqlalchemy.url"))
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
    # as the above options don't affect the below cmds I just have to change the url in env.py when testing or not

    
    # command.current(alembic_cfg, verbose=True)
    # command.history(alembic_cfg, verbose=True)
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    db = SessionLocal_test_db()
    try:
        yield db
    finally:
        db.close()
# here we override our original data stores so that our requests are made to our test data stores
@pytest.fixture
def test_client(session_db):
    def override_start_redis():
        r1_client = redis.Redis(
        host='localhost',
        port=6379, db=2)
        try:
            yield r1_client
        finally:
            None
        
    def override_get_db():

        try:
            yield session_db
        finally:
            session_db.close()

    app.dependency_overrides[start_redis] = override_start_redis
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
@pytest.fixture
def user_ronald(test_client):
    user_data = {"email":"rawrgunz55@gmail.com", "password": "natalia"}
    res = test_client.post('/users/', json=user_data)
    res_user_data = res.json()
    res_user_data['password'] = user_data['password']
    return res_user_data

@pytest.fixture
def user_ronald2(test_client):
    user_data = {"email":"rainwave5@gmail.com", "password": "natalia"}
    res = test_client.post('/users/', json=user_data)
    res_user_data = res.json()
    res_user_data['password'] = user_data['password']
    return res_user_data

@pytest.fixture
def token(user_ronald):
    encoded_jwt = jwt.encode({"user_id":user_ronald['userid']}, settings.secret_key_languages, algorithm=settings.algorithm_languages)
    encoded_jwt = create_access_token({"user_id":user_ronald['userid']})
    return encoded_jwt

@pytest.fixture
def auth_client(test_client, token):
    test_client_copy = test_client
    test_client_copy.headers.update({"Authorization":f"Bearer {token}"})
    test_client_copy.headers
    authenticated_client = test_client_copy
    return authenticated_client

@pytest.fixture
def test_languages(user_ronald, session_db, user_ronald2):
    lang_data = [
        {"name":"Français", "origin":"france", "description":"une langue que j'apprècie beaucoup", "userid": user_ronald['userid']},
        {"name":"Anglais", "origin":"inglaterre", "description":"une langue que je parle beaucoup", "userid": user_ronald['userid']},
        {"name":"Espagnole", "origin":"france", "description":"une langue que j'aime beaucoup", "userid": user_ronald['userid']},
        {"name":"Chinois", "origin":"chine", "description":"une langue que j'aimerais beaucoup apprendre bientôt", "userid": user_ronald2['userid']}
    ]
    new_models = [models.LanguageModel(**data) for data in lang_data]
    session_db.add_all(new_models)
    session_db.commit()
    # the refresh no longer applies I just have to search the id
    # res_models = [session_db.refresh(a_model) for a_model in new_models]
    # return session_db.refresh(new_models[0])
    
    