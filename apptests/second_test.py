from pydantic.types import Json
import pytest
from basicfunction import Language_Learner, lies
from jose import jwt
from fastapiapp.config import settings
from fastapiapp.oauth2 import create_access_token

@pytest.fixture
def ronald():
    ronaldd = Language_Learner(initial_languages={'Anglais': 'langue maternelle', 'Espagnole':'Deuxième langue', 'Francais':'Troisième Langue'})
    return ronaldd


@pytest.mark.parametrize("lang, desc, res", [
    ('francais', 'une langue', {'francais': 'une langue'}),
    # ("2+4", 6),
    # ("6*9", 42)
    ])
def test_add_language(lang, desc, res):
    ronald = Language_Learner()
    ronald.add_language(lang, desc)
    assert ronald.known_languages == res

@pytest.mark.parametrize("lang, desc, res", [
    ('francais', 'une langue', {'francais': 'une langue'}),
    # ("2+4", 6),
    # ("6*9", 42)
    ])
    
def test_forget_language(lang,desc,res):
    with pytest.raises(lies) as exc_info:
        ronald = Language_Learner()
        ronald.add_language(lang, desc)
        forgotten_lang = ronald.forget_language('Francais') #could try francais
        assert ronald.known_languages == {}

def test_cls_method():
    ron = Language_Learner.class_method_test(initial_languages={'anglais':'une langue'}, lang='anglais')
    assert ron.known_languages == {}
    assert type(ron) == Language_Learner
    

def test_lang_keys(ronald):
    langue = ronald.forget_language('Francais')
    assert ronald.last_forgotten_lang == 'Francais'
    assert list(ronald.known_languages.keys()) == ['Anglais','Espagnole']



def test_home(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_crear_usuario(test_client):
    # with pytest.raises(HTTPException) as exc_info:
    res = test_client.post('/users/', json={"email":"rainwave5@gmail.com", "password": "natalia"})
    # assert res.status_code = HTTPException()
    assert res.status_code == 201

def test_crear_usuario_ya_creado(test_client, user_ronald):
    # with pytest.raises(HTTPException) as exc_info:
    res = test_client.post('/users/', json={"email":user_ronald['email'], "password": user_ronald['password']})
    # assert res.status_code = HTTPException()
    assert res.status_code == 500

def test_login(test_client, user_ronald):
    # with pytest.raises(HTTPException) as exc_info:
    res = test_client.post('/login', data={"username":user_ronald['email'], "password": user_ronald['password']})
    # assert res.status_code = HTTPException()
    assert res.status_code == 200
    token = res.json()['access_token']
    payload = jwt.decode(token, settings.secret_key_languages, algorithms=[settings.algorithm_languages])
    id = payload.get("user_id")
    assert id == user_ronald['userid']

# attempt to create an authorized session
# create a token
# I want to place said token in the headers


def test_post_language(auth_client, user_ronald):  
    lang_data = {"name":"Français", "origin":"france", "description":"une langue que j'apprècie beaucoup"}
    res = auth_client.post("/languages/", json=lang_data)
    
    assert res.status_code == 201
    assert res.json()['user']['userid'] == user_ronald['userid']
    # print(res.json())