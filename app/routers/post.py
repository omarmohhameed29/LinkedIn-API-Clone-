from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db
from typing import List

router = APIRouter()


@router.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@router.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    raise HTTPException(404, 'ID not found')


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_item = models.Post(**post.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item





@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
        
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
@router.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID Not Exists')

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
