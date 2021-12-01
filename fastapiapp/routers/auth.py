from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from ..db import get_db
from .. import models , schemas, utils, oauth2
from sqlalchemy.orm import Session





router = APIRouter(tags=['Authorization'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    fetched_user = db.query(models.UserModelORM).filter(models.UserModelORM.email == user_credentials.username).first()
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong account credentials")
    
    verify_request = utils.verification(user_credentials.password, fetched_user.password)
    if not verify_request:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="wrong account credentials") 
    token = oauth2.create_access_token(user_data = {"user_id": fetched_user.userid})
    return {"access_token": token, "token_type": "bearer"}
