from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "I like pizza", "id": 2}
]

@app.get('/')   # @<app name>.<method>('</path>')
def root():
    return{'message': 'Welcome to our website'}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()



@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    db_item = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if post:
        return {"Data": post}
    raise HTTPException(404, 'ID not found')


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")

    # If the post is found, delete it (you may want to implement the deletion logic here)
    # For now, the code raises a 204 No Content response without deleting anything
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content,id))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID Not Exists')

    return {"Message": update_post}