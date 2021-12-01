from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.sql.functions import func

from ..db import get_db
from .. import models , schemas, utils
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["User"]
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserModelResponseSchema)
def create_user(user_data: schemas.UserModelSchema, db: Session = Depends(get_db)):

    fetched_user = db.query(models.UserModelORM).filter(models.UserModelORM.email == user_data.email).first()
    if fetched_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="This email is already taken")
    user_data.password = utils.get_password_hash(user_data.password)
    user = models.UserModelORM(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{id}", response_model=schemas.UserModelResponseSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModelORM).filter(models.UserModelORM.userid==id).first()
    user_q = db.query(models.UserModelORM, func.count().label("please")).join(models.LanguageModel, models.UserModelORM.userid == models.LanguageModel.userid).group_by(models.UserModelORM.userid)
    print(user_q)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user id {id} does not exist")
    return user