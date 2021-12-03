from fastapi import Depends, HTTPException, status, APIRouter, Response

from ..db import get_db
from .. import models , schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..schemas import SpokenLanguageSchema


router = APIRouter(prefix="/spokenlanguages",
tags=["SpokenLanguages"])

# edit so that the right codes are sent
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SpokenLanguageResponseSchema)
def post_spoken_language(language: schemas.SpokenLanguageSchema, db: Session = Depends(get_db), user: models.UserModelORM = Depends(oauth2.get_current_user) ):
    lang_query = db.query(models.LanguageModel).filter(models.LanguageModel.name == language.name)
    lang = lang_query.first()
    if not lang:
        # maybe allow a language to be created
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="language doesn't exist")

    spoken_language_query = db.query(models.SpokenLanguageLinkModelORM).filter(models.SpokenLanguageLinkModelORM.LanguageID == lang.languageid, 
    models.SpokenLanguageLinkModelORM.UserID == user.userid)
    spoken_language = spoken_language_query.first()

    if spoken_language and language.active == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already speak this language")
    elif not spoken_language and language.active == 1:
        
        link_lang = models.SpokenLanguageLinkModelORM(UserID=user.userid, LanguageID=lang.languageid)
        db.add(link_lang)
        db.commit()
        db.refresh(link_lang)
        return link_lang
    


    if (spoken_language or not spoken_language) and language.active == 0:
        spoken_language_query.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="deleted")

