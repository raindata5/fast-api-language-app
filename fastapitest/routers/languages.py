
from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter


from ..db import engine, get_db
from .. import models , schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import column, text, func
from ..config import Settings

router = APIRouter(
    prefix='/languages',
    tags=['Language']
)

# not sure if explicitly declaring user input as text() is safe... must confirm 
# either way I can just hardcode my own order by criteria since the purpose of this is just to offset and not sort
# the model in query is similar to the the table that would be in the from clause in the sense that the first argument in join can't 
# be the same table but the one to which it is joined

# the best I can get in a joined query is including certain columns from the tables rather than bring through relationships
# could possibly look to implement a windowing function SUCCCCESSS!
# just create new responsemodelschema and do the same for individual languages
@router.get("/", response_model= List[schemas.LanguageSpeakersResponseSchema])
def get_languages(limit: Optional[int] = None , offset: Optional[int] = None, keyword: Optional[str] = '', sort: Optional[str] = '', db: Session = Depends(get_db)):
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
def get_language(id: int, db: Session = Depends(get_db)):
    # fetch_query = db.query(models.LanguageModel).filter(models.LanguageModel.languageid == id)
    # lang = fetch_query.first()
    lang = db.query(models.LanguageModel, func.count(models.SpokenLanguageLinkModelORM.UserID).over(partition_by=models.SpokenLanguageLinkModelORM.LanguageID).label("Speakers")).join(
        models.SpokenLanguageLinkModelORM, models.LanguageModel.languageid == models.SpokenLanguageLinkModelORM.LanguageID
        , isouter=True).filter(models.LanguageModel.languageid == id).first()
    if lang is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="lang not found bro")    
    return lang


# data returned by user_id: schemas.TokenData =  Depends(oauth2.get_current_user) is <class 'fast-api-test.schemas.TokenData'> (id=3)
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_lang(lang_data: schemas.LanguageModelSchema, db: Session = Depends(get_db), user_obj: schemas.UserModelSchema =  Depends(oauth2.get_current_user)):
    lang_data = lang_data.dict()
    lang_data['userid'] = user_obj.userid
    lang_created = models.LanguageModel(**lang_data)
    user_obj.userid
    db.add(lang_created)
    db.commit()
    db.refresh(lang_created)
  
    return lang_created

 # come back and make put itempotent
@router.put("/{id}", response_model=schemas.LanguageModelResponseSchema)
def put_lang(lang_data: schemas.LanguageModelSchema, id: int, db: Session = Depends(get_db), user_obj: schemas.UserModelSchema =  Depends(oauth2.get_current_user)):
    fetch_query = db.query(models.LanguageModel).filter(models.LanguageModel.languageid == id)
    lang = fetch_query.first()
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can't delete someone else's post")
    # db.delete(lang) this seems to work as well
    fetch_query.delete(synchronize_session=False)
    db.commit()
    return {"msg":"language deleted"}