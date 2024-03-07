# uvicorn app.main:app --reload
# run container: docker run --network host -it linkedin_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 


from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')   # @<app name>.<method>('</path>')
def root(): 
    return{'message': 'Welcome to LinkedIn API'}



