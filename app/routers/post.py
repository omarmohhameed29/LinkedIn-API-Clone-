from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, isouter=True)\
            .group_by(models.Post.id).all()
    return result


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).filter(models.Post.id == id).join(models.Vote, isouter=True).group_by(models.Post.id)
    print(post)
    if not post:
        raise HTTPException(404, 'ID not found')

    return post.first()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    db_item = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item





@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')
            
    post_query.delete(synchronize_session=False)
    db.commit()
    
@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID Not Exists')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
