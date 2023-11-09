### About Fast API
*Very fast compared to django and flask due to asynchronous code execution*

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