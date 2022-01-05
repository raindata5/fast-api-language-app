
import json
from fastapiapp import schemas
import pytest

def test_get_languages(auth_client, test_languages):
    res = auth_client.get("/languages/")
    assert res.status_code == 200
    # print(res.json())
    lang_responses = [schemas.LanguageSpeakersResponseSchema(**model) for model in res.json()]
    print(lang_responses[1])

@pytest.mark.parametrize("name, origin, description",[
    ("Français", "france", "une langue que j'apprècie beaucoup"),
    ("Espagnole", "espagne", 'j\'aime bien'),
    ("russe", "russie",'j\'suis pas sur que ça s\'appele la russie')
])
def test_post_language(auth_client, user_ronald, name, origin, description):
    lang_data = {"name":name, "origin":origin, "description":description}
    res = auth_client.post("/languages/", json=lang_data)
    assert res.status_code == 201
    assert res.json()['user']['userid'] == user_ronald['userid']

def test_unauth_user_post_lang(test_client):
    lang_data = {"name":"Français", "origin":"france", "description":"une langue que j'apprècie beaucoup"}
    res = test_client.post(f"/languages/", json=lang_data)
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'

def test_unauth_user_get_lang_with_redis(test_client, test_languages):
    # lang_data = {"name":"Français", "origin":"france", "description":"une langue que j'apprècie beaucoup"}
    res = test_client.get(f"/languages/1")
    # assert res.status_code == 200
    # res = test_client.get("/languages/")
    res = test_client.get(f"/languages/1")
    print(res)

def test_unauth_user_del_lang(test_client, test_languages):
    res = test_client.delete(f"/languages/{1}")
    assert res.status_code == 401

def test_del_post(auth_client,test_languages):
    res = auth_client.delete(f"/languages/{1}")
    assert res.status_code == 204

def test_del_post_not_found(auth_client,test_languages):
    res = auth_client.delete(f"/languages/{25}")
    assert res.status_code == 404

def test_auth_user_del_lang_of_diff_user(auth_client, test_languages):
    res = auth_client.delete(f"/languages/{4}")
    assert res.status_code == 401
    print(res.json())

def test_update_lang(auth_client,test_languages):
    data = {"name":"Français", "origin":"france", "description":"une langue que j'apprècie énormement"}
    res = auth_client.put(f"/languages/{1}", json=data)
    assert res.status_code == 200
    new_post = schemas.LanguageModelSchema(**res.json())
    assert new_post.description == "une langue que j'apprècie énormement"

def test_update_lang_of_diff_user(auth_client,test_languages):
    data = {"name":"Français", "origin":"france", "description":"une langue que j'apprècie énormement"}
    res = auth_client.put(f"/languages/{4}", json=data)
    assert res.status_code == 401

def test_unauth_user_update_lang_of_diff_user(test_client, test_languages):
    lang_data = {"name":"Français", "origin":"france", "description":"une langue que j'apprècie beaucoup"}
    res = test_client.put(f"/languages/{4}", json=lang_data)
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'