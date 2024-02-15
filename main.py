from fastapi import FastAPI

app = FastAPI()

@app.get('/')   # @<app name>.<method>('</path>')
def root():
    return{'message': 'Welcome to our website'}

@app.get('/posts')
def get_posts():
    return {'data': 'this is new post'}


# will not appear, the first path only executes
@app.get('/posts')
def get_posts():
    return {'data': 'this is second post'}