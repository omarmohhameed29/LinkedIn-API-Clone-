from app import schemas
from .database import client, session

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to LinkedIn API'}


def test_create_user(client):
    response = client.post('/users/', json={"email":"omarmo@gmail.com", "password": "omarmo"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "omarmo@gmail.com"
    assert response.status_code == 201

def test_user_login(client, session):
    response = client.post('/login', data={"username": "omarmo@gmail.com", "password": "omarmo"})
    assert response.status_code == 200