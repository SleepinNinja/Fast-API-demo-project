# Fast API
* *Very fast compared to django and flask as it is based on starlette(Light weight asgi framework ideal for building async web services in python) and pydantic(data validation library in python).*

* *Auto documentation: By default provides Swagger UI for api documentation, it also provides ReDoc apart from Swagger UI*

* *Using morden python features like python 3.6 with type using pydantic.*

* *Based on open standards like JSON Schema and Open API.*

* *Security and autentication like Basic HTTP OAuth2(also with jwt tokens), API keys in headers, query parameters, cookies etc.*

* *We also have dependency injection, unlimited plug-ins and testing support.*

* *Fast API also uses Starlette features which include, websockets, graphql support, in-process background tasks, startup and shutdown events, test-client built on request, CORS, GZip, Static Files, Streaming responses, Session and Cookie Support etc etc.*

* *SQL database, NoSQL database and GraphQL is also supported.*


### Running FastAPI Server.
```py
uvicorn main:app --reload
```
Here main is the main file name and app is the FastAPI class instance.


```py
@8app.get('/')
def home():
    return 'This is home page.'
```
1. Here in FAST API the endpoints are called path.
2. get() is the operation performed on the path.
3. def home() this is called the path operation 
4. function which operates on the given path for given operation.
5. @app is called path operation decorator.


### Dynamic routing in FastAPI
*Whenever we want to use dynamic routes we can use {id}*

```py
@app.get('/blog/{id}')
def show(id):
    return {
        'data': id
    }
```

### Path Parameter and Typing in FastAPI
*In FastAPI we can provide typing of the variables we accept so that it can automatically type converted when we access in the function*

```py
@app.get('/blog/{id}')
def show(id: int):
    return {
        'data': id
    }
```
*From browser id is accepted as int but as we have provided typing this id will automatically get converted into int when we access id in the path operation function, also this id will be only accepted as string and if we try to provide some other value then it will return an error json.*

```py
@app.get('/blog/any')
def show_any(id: int):
    return {
        'data': id
    }
```

*This block of code will raise error because FastAPI mathces path in the order they are written in the main file, to /blog/{id} means match blog/anything and this mathces the any in the above url and raises an error.*


### The data validation is done using Pydantic.
*Pydantic provides data validation of normal as well as complex types.*


### Accessing the Swagger UI and Redoc
*The Swagger UI are available at /docs path and Redoc is available at /redoc path.*

### Query Parameter
```py
@app.get('/blogs')
def blog(limit:int=10, published:bool=True, sort: Optional[str]=None):
    return f'Returning {limit} blogs with published set to {published}'

```

*The above path operator function will use `http://127.0.0.1:8000/blogs?limit=20&published=True` this path to accept as query parameter in the function. The query parameter must be passed in the url or must have a default value, if query parameter is not actually required we can give it as Optional[type] where type is the type hint of the optional query parameter value.*

`*Fast API first detects path parameters then query parameters.*`


### Request Body
*Whenever we want to send a request body we need to create a pydantic model and are defined using a :*

```py
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] 


@app.post('/blog')
def create_blog(blog:Blog):
    return {'data': f'blog created with {blog}'}
```

*This is how models are created to accept and and return response in the request body and response body*


### Debugging
We can use VS Code debugging tool for debugging of our Fast API project.

### Running Fast API server on some other port
```py
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=9000)
```
*Now this will work on localhost and port 9000*


### CRUD operations using Fast API.

```py
uvicorn blog.main:app --reload
```
*This is used for running the main file inside the blog app, also Sqlalchemy is one of the packages that used for performing CRUD operations on the database*

```py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declerative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(
    echo=SQLALCHEMY_DATABASE_URL,
    connection_args={
        'check_same_thread': False,
    }
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declerative_base()
```
*Here we have completed our database connections, if we don't specify database URI and db name then it will store everything in memeory.*

### Models and Tables
*As we are using Sqlalchemy we will create modles which will contain all the columns that needs to be present in that table.*

```py
from .database import Base
from sqlalchemy import Column, Integer, String


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
```

*Providing tablename is important else error is raised, also this tablename is the name of the table in our database.*

```py
models.Base.metadata.create_all(engine)
```

*This line is very important as it creates the tables it the database as defined in the models.py*

```py
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.post('/blog')
def create(request: Blog, db: Session=Depends(get_db)):
    return request
```

*This block of code means that db is type Session and the default_value depends on the the function get_db, if default value is not given then pydantic raises error.*

### Create Operation
```py
@app.post('/blog')
def create(request: Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(
        title = request.title,
        body = request.body
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
```

## Read Operation

```py
@app.get('/blog')
def all_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
```

```py
@app.get('/blog/{id}')
def blog(id: int=1, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog
```


### Delete Operation

```py

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {id} does not exits.'
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return {
        'message': f'Blog with id {id} is deleted.'
    }
```

### Update Operation
```py
def raise_not_found(id:int=None):
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exists.'
        )

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int, request: Blog, db: Session=Depends(get_db)):
    print('calling blog update')
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise_not_found(id=id)
    blog.update(request.dict())
    db.commit()
    return f'Blog with id {id} updated successfully with data {request}'
    
```

### Exception and Response Codes.

```py
from fastapi import HTTPException, Response


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def blog(response:Response, id: int=1, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} does not exists.'
        )
        # * this can also be done using the below two lines
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} does not exits.'}
    return blog
```

### Response Model

*Using response model we can define a model for a response. In pydantic the correct terminology is Schema and not model. `The Sqlalchemy ones are called models and the pydnatic ones are called schemas`. There the response schema is response model. This response model is used for specifying the model fields to be show in the response.*

```py
class ShowBlog(Blog):
    class Config:
        from_attributes = True
```

```py
@app.get('/blog/{id}', response_model=ShowBlog, status_code=status.HTTP_200_OK)
def blog(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise_not_found(id=id)
    return blog
```

*Now the response will only show name and body attributes of the blog model in response.*
