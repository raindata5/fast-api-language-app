
from typing import Any, List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter

from datetime import timedelta
from ..db import engine, get_db, start_redis
from .. import models , schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import column, text, func
from ..config import Settings
import json


router = APIRouter(
    prefix='/languages',
    tags=['Language']
)

# not sure if explicitly declaring user input as text() is safe...(not safe)
# either way I can just hardcode my own order by criteria since the purpose of this is just to offset and not sort
# the model in query is similar to the the table that would be in the from clause in the sense that the first argument in join can't 
# be the same table but the one to which it is joined

# the best I can get in a joined query is including certain columns from the tables rather than bring through relationships
# could possibly look to implement a windowing function SUCCCCESSS!
# just create new responsemodelschema and do the same for individual languages
@router.get("/", response_model= List[schemas.LanguageSpeakersResponseSchema])
def get_languages(limit: Optional[int] = None , offset: Optional[int] = None, keyword: Optional[str] = '', sort: Optional[str] = '', db: Session = Depends(get_db), redis_client: Session = Depends(start_redis)):
    langs = db.query(models.LanguageModel).filter(models.LanguageModel.description.contains(keyword)).order_by(text(sort)).limit(limit).offset(offset).all()
    # sql server is a bit more strict with the group by statement and the columns it allows to be returned while postgres not so much
    # results = db.query(models.LanguageModel.languageid, models.LanguageModel.name, func.count().label("please")).join(models.SpokenLanguageLinkModelORM, models.LanguageModel.languageid == models.SpokenLanguageLinkModelORM.LanguageID).group_by(models.LanguageModel.languageid, models.LanguageModel.name ).all()
    # results = db.query(models.SpokenLanguageLinkModelORM.LanguageID, func.count().label("please")).join(models.LanguageModel, models.LanguageModel.languageid == models.SpokenLanguageLinkModelORM.LanguageID).group_by(models.SpokenLanguageLinkModelORM.LanguageID).all()
    results = db.query(models.LanguageModel, func.count(models.SpokenLanguageLinkModelORM.UserID).over(partition_by=models.SpokenLanguageLinkModelORM.LanguageID).label("Speakers")).join(
        models.SpokenLanguageLinkModelORM, models.LanguageModel.languageid == models.SpokenLanguageLinkModelORM.LanguageID, isouter=True).filter(models.LanguageModel.description.contains(keyword)).order_by(text(sort)).limit(limit).offset(offset).all()
    # return langs
    return results

# originally used schemas.LanguageModelResponseSchema
@router.get("/{id}", response_model=schemas.LanguageSpeakersResponseSchema)
def get_language(id: int, db: Session = Depends(get_db), redis_client: Any = Depends(start_redis)):
    # fetch_query = db.query(models.LanguageModel).filter(models.LanguageModel.languageid == id)
    # lang = fetch_query.first()
    try:
        print(redis_client)
        cached_language_data = None
        cached_language_data = redis_client.get(f"language:{id}")
    except Exception as e:
        print(e)

    if cached_language_data: # maybe provide another if just to see if the user dat ais present as well
        try:
            cached_language_data = json.loads(cached_language_data)
            user_id = cached_language_data['userid']

            cached_user_data = redis_client.get(f"user:{user_id}")
            cached_user_data = json.loads(cached_user_data)


            s = cached_language_data['Speakers'] # place speakers in a variable
            cached_language_data.pop('Speakers',1) # removes speakers from the dictionary
            cached_language_data['user'] = cached_user_data # adding the user model data to what will become our language model
            LanguageModel = models.LanguageModel(**cached_language_data) # creating language model (userid still prsent)
            LanguageModel # this is now a language model
            print('Used Redis')
            return {'LanguageModel':LanguageModel, 'Speakers': s}
        except Exception as e:
            print(e)



    lang = db.query(models.LanguageModel, func.count(models.SpokenLanguageLinkModelORM.UserID).over(partition_by=models.SpokenLanguageLinkModelORM.LanguageID).label("Speakers")).join(
        models.SpokenLanguageLinkModelORM, models.LanguageModel.languageid == models.SpokenLanguageLinkModelORM.LanguageID
        , isouter=True).filter(models.LanguageModel.languageid == id).first()
    if lang is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="lang not found bro")

    # breaking up the models
    lang_model=lang.LanguageModel
    user_model = lang.LanguageModel.user
    # converting the models into a python dictionaries
    lang_model_dict_dumped = schemas.dict_request(lang_model, inc_json_dump=False)
    user_model_dict_dumped = schemas.dict_request(user_model, inc_json_dump=False)
    # adding speakers back to dictonary that contains language model
    lang_model_dict_dumped['Speakers'] = lang.Speakers
    # getting the userid so it can be request agnostic
    user_id = user_model.userid
    # potential issue is data expirations being ofset by requests on other endpoints
    redis_client.set(f"user:{user_id}", json.dumps(user_model_dict_dumped))
    redis_client.expire(f"user:{user_id}", timedelta(seconds=10))
    redis_client.set(f"language:{id}", json.dumps(lang_model_dict_dumped))
    redis_client.expire(f"language:{id}", timedelta(seconds=10))
    print('Used Postgres')

    return lang


# data returned by user_id: schemas.TokenData =  Depends(oauth2.get_current_user) is <class 'fast-api-test.schemas.TokenData'> (id=3)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LanguageModelResponseSchema)
def post_lang(lang_data: schemas.LanguageModelSchema, db: Session = Depends(get_db), user_obj: schemas.UserModelSchema =  Depends(oauth2.get_current_user)):
    lang_data = lang_data.dict()
    lang_data['userid'] = user_obj.userid
    lang_created = models.LanguageModel(**lang_data)
    user_obj.userid
    db.add(lang_created)
    db.commit()
    db.refresh(lang_created)
  
    return lang_created

 # come back and make put idempotent
@router.put("/{id}", response_model=schemas.LanguageModelResponseSchema)
def put_lang(lang_data: schemas.LanguageModelSchema, id: int, db: Session = Depends(get_db), user_obj: schemas.UserModelSchema =  Depends(oauth2.get_current_user)):
    fetch_query = db.query(models.LanguageModel).filter(models.LanguageModel.languageid == id)
    lang = fetch_query.first()
    # here language needs to be created
    if lang is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="lang not found bro")
    if lang.userid != user_obj.userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can't edit someone else's post")
    fetch_query.update(lang_data.dict())    
    db.commit()
    return fetch_query.first()
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_lang(id: int, db: Session = Depends(get_db), user_obj: schemas.UserModelSchema =  Depends(oauth2.get_current_user)):
    fetch_query = db.query(models.LanguageModel).filter(models.LanguageModel.languageid == id)
    lang = fetch_query.first()
    if lang is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="lang not found bro")
    if lang.userid != user_obj.userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can't delete someone else's language")
    # db.delete(lang) this seems to work as well
    fetch_query.delete(synchronize_session=False)
    db.commit()
    return {"msg":"language deleted"}