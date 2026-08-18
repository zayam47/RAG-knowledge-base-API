# FastAPI Basics

FastAPI is a modern Python web framework for building APIs. It is built on
top of Starlette for the web handling parts and Pydantic for data
validation. A key feature of FastAPI is automatic request validation: when
you define an endpoint with typed parameters, FastAPI checks incoming
requests against those types and returns a clear error if they don't match.

FastAPI automatically generates interactive API documentation. Once your
app is running, you can visit /docs to get a Swagger UI page, or /redoc for
an alternative documentation layout. Both are generated from your route
definitions and Pydantic models without any extra work.

Path parameters in FastAPI are declared directly in the route decorator,
for example @app.get("/items/{item_id}"), and the corresponding function
argument is automatically parsed and validated based on its type hint.
Query parameters are declared as regular function arguments that are not
part of the path.

Dependency injection is a core part of FastAPI's design. You can define a
function that provides some resource (like a database session or the
current authenticated user) and then inject it into any route using
Depends(). This keeps route functions focused on business logic and makes
testing easier, since dependencies can be overridden.

FastAPI supports asynchronous route handlers using async def. When a route
performs I/O-bound work such as calling a database or an external API,
defining it as async allows the server to handle other requests while
waiting, improving throughput under load.

Pydantic models are used to define the shape of request bodies and
responses. A model is a Python class that inherits from BaseModel, with
typed fields. FastAPI uses these models both to validate incoming JSON and
to serialize outgoing responses, and it will reject a request body that
doesn't match the expected schema.
