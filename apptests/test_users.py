from fastapiapp import schemas
from pydantic.networks import EmailStr
import datetime

from alembic.config import Config
from alembic import command
from fastapiapp.config import settings
import pytest
from jose import jwt



@pytest.fixture
def test_user(test_client):
    user_data = {"email": "rawrgunz55@gmail.com", "password": "airflow"}
    res = test_client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user



def test_home(test_client,test_user):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Connected ^_^"}




# these tests actually create users
# def test_user_creation(test_client, test_user):
#     # with pytest.raises(HTTPException) as exc_info:
#     res = test_client.post('/users/', json={"email": "rawrgunz55@gmail.com", "password": "airflow"})
#     print(res.json())
#     assert res.json().get("email") == EmailStr('rawrgunz55@gmail.com')
#     ronald = schemas.UserModelResponseSchema(**res.json())
#     assert type(ronald.created_at) == datetime.datetime
#     assert res.status_code == 201


def test_user_email_taken(test_client, test_user):
    # with pytest.raises(HTTPException) as exc_info:
    res = test_client.post('/users/', json={"email": test_user['email'], "password": test_user['password']})
    assert res.status_code == 500


def test_user_login(test_client, test_user):
    res = test_client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_res_schema = schemas.Token(**res.json())
    payload = jwt.decode(login_res_schema.access_token, settings.secret_key_languages, algorithms=[settings.algorithm_languages])    
    id = payload.get("user_id")
    assert id == test_user['userid']
    assert login_res_schema.token_type == "bearer"
    assert res.status_code == 200

def test_failed_login(test_client, test_user):
    res = test_client.post("/login", data = {"username": test_user.get('email'), "password": 'paperplanes'})
    assert res.status_code == 403
    assert res.json().get('detail') == "wrong account credentials"

@pytest.mark.parametrize("email, password, status_code",[
    ("rawrgunz55@gmail.com", "airflow", 200),
    ("rawrgunz55@gmail.com", "airflow123", 403),
    ("rawrgunz5@gmail.com", "airflow",403),
    ('', "airflow", 422)
])
def test_one(test_client, test_user, email, password, status_code):
    res = test_client.post("/login", data = {"username": email, "password": password})
    assert res.status_code == status_code


