from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from .schemas import Blog
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . import models

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

def raise_not_found(id:int=None):
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exists.'
        )

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(
        title = request.title,
        body = request.body
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def list_blog(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def blog(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise_not_found(id=id)
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise_not_found(id=id)
    blog.delete(synchronize_session=False)
    db.commit()
    return f'Blog with id {id} updated successfully deleted.'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int, request: Blog, db: Session=Depends(get_db)):
    print('calling blog update')
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise_not_found(id=id)
    blog.update(request.dict())
    db.commit()
    return f'Blog with id {id} updated successfully with data {request}'
    
