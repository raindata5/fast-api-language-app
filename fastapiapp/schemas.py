from datetime import datetime
import json
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from email_validator import validate_email


class LanguageModelSchema(BaseModel):
    name: str
    origin: str
    description: Optional[str] = "C'est belle comme langue"

class UserModelSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class SpokenLanguageSchema(BaseModel):
    name: str
    active: bool



class UserModelResponseSchema(BaseModel):
    created_at: datetime
    email: EmailStr
    userid: int

    class Config:
        orm_mode = True 


class LanguageModelResponseSchema(LanguageModelSchema):
    languageid: int
    created_at: datetime
    user: UserModelResponseSchema
    class Config:
        orm_mode = True 

class SpokenLanguageResponseSchema(BaseModel):
    language: LanguageModelResponseSchema
    user: UserModelResponseSchema

    class Config:
        orm_mode = True


# made possible by a windowing function
class LanguageSpeakersResponseSchema(BaseModel):
    LanguageModel: LanguageModelResponseSchema
    Speakers: Optional[int] = 0

    class Config:
        orm_mode = True 

def dict_request(orm_model, inc_json_dump=False):
    d = {}
    for column in orm_model.__table__.columns:
        d[column.name] = str(getattr(orm_model, column.name))
    if not inc_json_dump:
        return d
    else:
        return json.dumps(d)


class testResponseSchema(BaseModel):
    LanguageModel: LanguageModelResponseSchema

    class Config:
        orm_mode = True 
