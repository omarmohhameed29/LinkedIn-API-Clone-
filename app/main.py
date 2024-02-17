from fastapi import FastAPI, Response, status, HTTPException
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
def get_posts():
    return {'data': my_posts}


# will not appear, the first path only executes
# @app.get('/posts')
# def get_posts():
#     return {'data': 'this is second post'}



@app.post('/posts', status_code=status.HTTP_201_CREATED)
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
    # response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(404, 'ID not found')


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Find the index of the post with the given ID
    index = find_post_index(id)

    # If the index is None, the post with the given ID was not found
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")

    # If the post is found, delete it (you may want to implement the deletion logic here)
    # For now, the code raises a 204 No Content response without deleting anything
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID Not Exists')

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"Message": post_dict}