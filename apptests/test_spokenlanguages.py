import json
from fastapiapp import schemas, models
import pytest

@pytest.fixture()
def test_spoken_lang(test_languages, session_db, user_ronald):
    #{"LanguageID":1, "UserID":user_ronald['userid']},
    spokens = [
    {"LanguageID":2, "UserID":user_ronald['userid']},
    {"LanguageID":3, "UserID": user_ronald['userid']}]
    spoken_models = [models.SpokenLanguageLinkModelORM(**spoken) for spoken in spokens]
    session_db.add_all(spoken_models)
    session_db.commit()

def test_auth_user_post_spoken_lang(auth_client, test_languages):
    res = auth_client.post("/spokenlanguages/", json = {"name":"Chinois", "active":1})
    assert res.status_code == 201

def test_auth_user_post_spoken_lang_already(auth_client, test_spoken_lang):
    res = auth_client.post("/spokenlanguages/", json = {"name":"Espagnole", "active":1})
    assert res.status_code == 409
    assert res.json()['detail'] == "You already speak this language"

def test_auth_user_del_spoken_lang(auth_client, test_spoken_lang):
    res = auth_client.post("/spokenlanguages/", json = {"name":"Espagnole", "active":0})
    assert res.status_code == 204

def test_auth_user_del_spoken_lang_not_found(auth_client, test_spoken_lang):
    res = auth_client.post("/spokenlanguages/", json = {"name":"Français", "active":0})
    assert res.status_code == 204

def test_auth_user_post_spoken_lang_lang_not_found(auth_client, test_spoken_lang):
    res = auth_client.post("/spokenlanguages/", json = {"name":"Japonais", "active":0})
    assert res.status_code == 404
    assert res.json()['detail'] == "language doesn't exist"

def test_unauth_user_post_spoken_lang(test_client, test_languages):
    res = test_client.post("/spokenlanguages/", json = {"name":"Chinois", "active":1})
    assert res.status_code == 401
    print(res.json())