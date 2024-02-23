from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import List

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    return db.query(models.Post).all()


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    raise HTTPException(404, 'ID not found')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    print(user_id)
    db_item = models.Post(**post.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item





@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
        
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID Not Exists')

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
