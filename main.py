from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def index():
    return 'hey'


@app.get('/about')
def about():
    return {
        'data': ['about page']
    }


@app.get('/blogs')
def blog(limit:int=10, published:bool=True, sort: Optional[str]=None):
    return f'Returning {limit} blogs with published set to {published}'


@app.get('/blog/{id}')
def show(id: int):
    return {
        'data': id
    }


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] 


@app.post('/blog')
def create_blog(blog:Blog):
    return {'data': f'blog created with {blog}'}