from datetime import datetime
from os import access
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
    Speakers: int

    class Config:
        orm_mode = True 