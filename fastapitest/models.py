from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATETIME
from sqlalchemy.orm import relationship
from .db import Base



class UserModelORM(Base):
    __tablename__ = "User"
    userid = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DATETIME(timezone=True), nullable = False, server_default=text('SYSUTCDATETIME()'))

class LanguageModel(Base):
    __tablename__ = 'Language'
    languageid = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)
    origin = Column(String, nullable=False)
    description = Column(String, server_default='C\'est belle comme langue')
    created_at = Column(DATETIME(timezone=True), server_default=text('SYSUTCDATETIME()'), nullable=False)
    userid = Column(Integer, ForeignKey("User.userid",ondelete="CASCADE"), nullable=False)
    user = relationship("UserModelORM")

class SpokenLanguageLinkModelORM(Base):
    __tablename__ = 'SpokenLanguage'
    UserID = Column(Integer, ForeignKey("User.userid",ondelete="CASCADE"),primary_key=True, nullable=False)
    LanguageID = Column(Integer, ForeignKey("Language.languageid"), primary_key=True, nullable=False)
    user = relationship("UserModelORM")
    language = relationship("LanguageModel")

