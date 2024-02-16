from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "I like pizza", "id": 2}
]

@app.get('/')   # @<app name>.<method>('</path>')
def root():
    return{'message': 'Welcome to our website'}

@app.get('/posts')
def get_posts():
    return {'data': my_posts}


# will not appear, the first path only executes
# @app.get('/posts')
# def get_posts():
#     return {'data': 'this is second post'}



@app.post('/posts')
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"Data of body": post_dict}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    for post in my_posts:
        if post['id'] == id: 
            return {"Curr post": post}
    # response.status_code = 404
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": 'Not Existed'}


