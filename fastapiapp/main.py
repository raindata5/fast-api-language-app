
from fastapi import FastAPI

from .routers import users, languages, auth, spokenlanguages

from .db import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)

origins =[
    "*"
]
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spokenlanguages.router)
app.include_router(users.router)
app.include_router(languages.router)
app.include_router(auth.router)

# @app.get("/sqlalchemytest")v
# def test(db: Session = Depends(get_db)):
#     print({'msg':'seems to work'})


