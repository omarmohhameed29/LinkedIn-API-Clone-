# uvicorn app.main:app --reload
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine

from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()







while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password=2912002, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connect to DB')
        break
    except Exception as e:
        print('Could not connect to DB')
        print(e)
        time.sleep(2)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get('/')   # @<app name>.<method>('</path>')
def root():
    return{'message': 'Welcome to our website'}



