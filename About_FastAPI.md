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
