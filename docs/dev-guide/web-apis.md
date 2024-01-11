# Web APIs

## Types

As a small aside, REST is not the only standard available when it
comes to web APIs.

### REST

REST has dominated the scene for quite a few years.

URLs are mapped to different HTTP methods (GET, POST, PUT, DELETE)
to perform an action when called.

Responses can be divided between Data APIs (return JSON) vs Hypermedia
APIs (return HTML).

### GraphQL

Without going into the details, this standard has many advantages over
REST Data APIs, with much more efficient queries being possible.

### RPC

The Remote Procedure Call (RPC) protocol can return XML or JSON responses.

It is used to trigger code remotely, so good for internal communication
between different services.
HOT uses gRPC for internal communication between tools, outside of their
REST API.

While a RESTful API returns a document, the response from an RPC server is
confirmation that the function was triggered, or an error indicating why
it failed to run.

### Others

SOAP is a historic API design using XML, and is no longer recommended.

### What To Choose

As of 2023, Data APIs have been key for the adoption of Single Page
Applications (SPA) and Javascript frameworks (where JSON data is manipulated
by the frontend).

Going forward, Hypermedia APIs are re-emerging as an increasingly important
alternative, where the entire page is rendered before being returned (reducing
the need for things like Server Side Rendering (SSR)).

The [HTMX](https://htmx.org/essays/) website has many interesting essays
on this topic.

**In summary, it is probably best to default to a Hypermedia REST API, with a
simple web framework like HTMX. If a much more complex frontend is required
(such as a word processor, graphics editor, complex map), then a Data REST API
is the best option**.

## Frameworks

API Frameworks are generally divided into synchronous and asynchronous.

Async is a newer paradigm in Python, often slightly more complex to code,
but should be faster and more suited to a web API.

Synchronous frameworks include **flask**, **Django**, etc.

The asynchronous framework we recommend at HOT, as of 2024, is **FastAPI**.
It's what we use for most projects.

There is a great [comparison](https://fastapi.tiangolo.com/alternatives/)
with other frameworks in the ecosystem available.

Another contender would be [LiteStar](https://github.com/litestar-org/litestar),
a project spawned from some frustrations with the governance of FastAPI.

### FastAPI

These docs provide some helpful info for FastAPI best practices.

#### Async Programming

Asynchronous programming can be a learning curve for Python developers.

- FastAPI is an asynchronous web framework that is built to use async code.
- Using async (`async def`) function with await is more scalable than
  using synchronous code `def`, so this is always the preferred default
  approach.
- Using synchronous code is possible, but devs should be aware of the pitfalls:
  if the code runs for a long time, it will block the async event loop
  (i.e. block the thread until the process completes).
  - Bear in mind that 'synchronous' code could be from what you write
    in the crud functions, OR could be from a library that you use
    (e.g. osm-fieldwork is synchronous for the most part).

#### Workers & Thread Blocking

- We run FastAPI (uvicorn) with a number of workers defined. This is the
  number of threads available to run processes.
- If a process blocks a thread (as described above), then the remaining threads
  are available to take new requests.
- If all of the workers/threads are blocked by tasks, the server will hang / be unresponsive!

#### Using Synchronous Code

It is of course possible to use synchronous code, but if necessary, be
sure to run this in another thread.

To do this you have several options.

#### Options

##### 1) Using sync code within an `async def` function

- Use the BackgroundTasks implementation we have, with polling for the
  task completion.
- The task should be written as a standard `def`. FastAPI will handle
  this automatically and ensure it runs in a separate thread.
- Alternatively, if you wish to run the task in the foreground and return
  the response, use the FastAPI helper `run_in_threadpool`:

```python
from fastapi.concurrency import run_in_threadpool

def long_running_sync_task(time_to_sleep):
    sleep(time_to_sleep)

async def some_func():
    data = await run_in_threadpool(lambda: long_running_sync_task(time_to_sleep))
```

##### 2) Running multiple standard `def` from within an `async def` function

- Sometimes you need to run multiple `def` functions in parallel.
- To do this, you can use ThreadPoolExecutor:

```python
from concurrent.futures import ThreadPoolExecutor, wait

def a_synchronous_function(db):
    # Run with expensive task via threadpool
    def wrap_generate_task_files(task):
        """Func to wrap and return errors from thread.

        Also passes it's own database session for thread safety.
        If we pass a single db session to multiple threads,
        there may be inconsistencies or errors.
        """
        try:
            generate_task_files(
                next(get_db()),
                project_id,
                task,
                xlsform,
                form_type,
                odk_credentials,
            )
        except Exception as e:
            log.exception(str(e))

    # Use a ThreadPoolExecutor to run the synchronous code in threads
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the thread pool
        futures = [
            executor.submit(wrap_generate_task_files, task)
            for task in tasks_list
        ]
        # Wait for all tasks to complete
        wait(futures)
```

Note that in the above example, we cannot pass the db object from the parent
function into the functions spawned in threads. A single database
connection should not be written to by multiple processes at the same time,
as you may get data inconsistencies. To solve this we generate a new
db connection within the pool for each separate task we run in a thread.

> To avoid issues, look into limiting the thread usage via:
> <https://stackoverflow.com/questions/73195338/how-to-avoid-database-connection-pool-from-being-exhausted-when-using-fastapi-in>

##### 3) Running an `async def` within a sync `def`

- As we try to write most functions async for FastAPI, sometime we need to
  run some `async def` logic within a sync `def`. This is not possible normally.
- To avoid having to write a duplicated `def` equivalent of the `async def`
  code, we can use the package `asgiref`:

```python
from asgiref.sync import async_to_sync

async def get_project(db, project_id):
    return something

def a_sync_function():
     get_project_sync = async_to_sync(get_project)
     project = get_project_sync(db, project_id)
     return project
```

##### 4) Efficiency running batch async tasks

- Sometime you may have a very efficient async task you need to call
  within a for loop.
- Instead of that, you can use `asyncio.gather` to much more efficiently
  collect and return the async data (e.g. async web requests, or async
  file requests, or async db requests):

```python
from asyncio import gather

async def parent_func(db, project_id, data, no_of_buildings, has_data_extracts):
    ... some other code

    async def split_multi_geom_into_tasks():
        # Use asyncio.gather to concurrently process the async generator
        split_poly = [
            split_polygon_into_tasks(
                db, project_id, data, no_of_buildings, has_data_extracts
            )
            for data in boundary_geoms
        ]

        # Use asyncio.gather with list to collect results from the
        # async generator
        return (
            item for sublist in await gather(*split_poly)
            for item in sublist if sublist
        )

    geoms = await split_multi_geom_into_tasks()
```

##### Note

- If you regularly find you are running out of workers/threads and the
  server is overloaded, it may be time to add a task queuing system to your stack.
- Celery is made for just this - defer tasks to a queue, and run gradually
  to reduce the immediate load.

#### Best Practices

##### 1. Logical Project Structure

- Group together related code into units.
- An example template could be:

```bash
fastapi-project
├── src
│   ├── projects
│   │   ├── routes.py  # endpoints + router
│   │   ├── schemas.py  # pydantic models
│   │   └── logic.py  # logic separate from routes for easier testing
│   ├── tasks
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── logic.py
│   ├── db
│   │   ├── models.py  # global database models (can also be per subdir)
│   │   ├── enums.py  # enum mapping for the database
│   │   └── database.py  # database connection config
│   ├── config.py  # global settings
│   └── main.py
├── tests/
```

##### 2. Use the Correct Response Type

- FastAPI has many in-built Response types:

  - HTMLResponse: this would be useful paired with a HTMX frontend.
  - JSONResponse: to return a JSON.
  - ORJSONResponse: a faster JSON encoder. If you need to encode a large number
    of object, this might be a good choice.
  - RedirectResponse: use this for linking to an S3 file, to avoid handling it
    in the FastAPI server (frontend goes directly to S3).
  - FileResponse: load an entire file from disk and serve to the user.
  - StreamingResponse: better for serving large file in chunks.

- Don't forget to include the correct HTTP `status_code` with your response:

  - 200: Success, used as the final return for most endpoints.
  - 204: Success, but no response data necessary.
  - 400: Bad request, usually malformed syntax or incorrect HTTP method (POST/GET).
  - 401: Unauthorized, if the client does did not provide an auth token.
  - 403: Forbidden, if the client does not have permission to access the content.
  - 404: Not found, if the requested content is not present. E.g. wrong project id.
  - 422: Unprocessable entity, if the request data is in the incorrect format.
    e.g. a string provided in a form body variable when it should be an int.
  - 500: Generic error if no other error is provided, like Exception in Python.

##### 3. Use Pydantic for Validation

###### Settings Config

```python
from functools import lru_cache
from typing import Any, Optional

from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main settings class, defining environment variables."""

    # Required field
    VAR1: str
    # Required field, but nullable
    VAR2: Optional[str]
    # Required field, with default
    VAR3: Optional[str] = "7050"
    # Not required field
    VAR4: Optional[str] = None

    DB_HOST: Optional[str] = "fmtm-db"
    DB_USER: Optional[str] = "fmtm"
    DB_PASSWORD: Optional[str] = "fmtm"
    DB_NAME: Optional[str] = "fmtm"

    FMTM_DB_URL: Optional[PostgresDsn] = None

    # Using a field validator to build a variable
    @field_validator("FMTM_DB_URL", mode="after")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        """Build Postgres connection from environment variables."""
        if isinstance(v, str):
            return v
        pg_url = PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_HOST"),
            path=info.data.get("DB_NAME", ""),
        )
        return pg_url

    # Using env_file param loads from .env
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", extra="allow"
    )

# lru_cache prevents building obj every time settings.var is invoked
@lru_cache
def get_settings():
    """Cache settings when accessed throughout app."""
    _settings = Settings()
    if _settings.DEBUG:
        print(f"Loaded settings: {_settings.model_dump()}")
    return _settings

settings = get_settings()
```

###### Model Validation

- Used for 'incoming' (user provided) data that needs to be validated.

```python
from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field, constr

class MusicBand(str, Enum):
   AEROSMITH = "AEROSMITH"
   QUEEN = "QUEEN"
   ACDC = "AC/DC"


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    username: constr(regex="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True)
    email: EmailStr
    age: int = Field(ge=18, default=None)  # must be greater or equal to 18
    # only "AEROSMITH", "QUEEN", "AC/DC" values are allowed to be inputted
    favorite_band: MusicBand = None
    website: AnyUrl = None
    valid_genre: Optional[boolean] = False

    @field_validator("valid_genre", mode="before")
    @classmethod
    def get_genre_from_band_name(cls, value: Any, info: ValidationInfo) -> str:
        """Get genre from band name."""
        if band := info.data.get("favorite_band"):
            log.debug(f"Determining genre from band {band}")
            genre = band_genre_mapping(band)
            if genre:
                return True
        return False
```

###### Model Data Serialization

- Used to format 'outgoing' data that is returned to a user.

```python
class TaskBase(BaseModel):
    """Base Task model to inherit."""
    # ConfigDict has many options
    # https://docs.pydantic.dev/latest/api/config/
    # E.g. use_enum_values automatically runs .value on enums
    # So a returned object will have
    #   `somefield: 1`
    # instead of
    #   `somefield: SomeEnum.TYPE1`
    model_config = ConfigDict(
        use_enum_values=True,
        validate_default=True,
    )

    # Exclude fields: for example we want to get these values from the database,
    # and then process them into different fields in our returned model.
    # outline (a WKB element from Postgis) --> outline_geojson
    outline: Any = Field(exclude=True)
    lock_holder: Any = Field(exclude=True)

    id: int
    outline_geojson: Optional[Feature] = None
    task_history: Optional[List[TaskHistoryBase]] = None


class TaskOut(TaskBase):
    """Task to return from endpoint."""

    locked_by_uid: Optional[int] = None
    outline_geojson: Optional[int] = None

    @field_serializer("locked_by_uid")
    def get_locked_by_uid(self, value: str) -> str:
        """Get lock uid from lock_holder details."""
        if self.lock_holder:
            return self.lock_holder.id
        return None

    @field_serializer("outline_geojson")
    def get_geojson_from_outline(self, value: Any, info: ValidationInfo) -> str:
        """Get outline_geojson from Shapely geom."""
        if outline := info.data.get("outline"):
            properties = {
                "fid": info.data.get("project_task_index"),
                "uid": info.data.get("id"),
                "name": info.data.get("project_task_name"),
            }
            log.debug("Converting task outline to geojson")
            return geometry_to_geojson(outline, properties, info.data.get("id"))
        return None
```

##### 4. FastAPI Dependencies (Depends)

###### Validation of additional constraints

- Pydantic can only validate the 'incoming' data from client input.
- Use dependencies (Depends) to validate input against other constraints:
  - Database constraints, such as project or email already exists, user not found.
  - Auth constraints, where the users level of authorization should be assessed
    in an endpoint.

Example:

```python
# logic.py (where the dependency is written)
async def valid_post_id(post_id: UUID4) -> Mapping:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


# routes.py (where Depends is used)
@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post: Mapping = Depends(valid_post_id)):
    return post


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    update_data: PostUpdate,
    post: Mapping = Depends(valid_post_id),
):
    updated_post: Mapping = await service.update(id=post["id"], data=update_data)
    return updated_post
```

If we didn't put data validation in a dependency, we would have to do the same
checks for on each endpoint (duplicating code).

###### Reuse & chain dependencies

- Dependencies can use other dependencies and repeating code.

Example:

```python
# logic.py
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Depends on pre-existing FastAPI dependency OAuth2PasswordBearer
async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}

# Depends on parse_jwt_data (chained)
async def valid_owned_post(
    post: Mapping = Depends(valid_post_id),
    token_data: dict = Depends(parse_jwt_data),
) -> Mapping:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()

    return post

# routes.py (where the final Depends is used)
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(post: Mapping = Depends(valid_owned_post)):
    return post
```

###### Dependency call are cached

- Dependencies can be reused multiple times, and they won't be recalculated.
- FastAPI caches dependency's result within a **request's scope** by default:
  - If a dependency makes a DB call, this can be cached when the dependency is
    called again.
  - With this in mind, try to de-couple dependencies, i.e. write smaller
    functions that do specific things, then chain them.

Example:

```python
# logic.py (contains dependencies here)
from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


# Dependency 1
async def valid_post_id(post_id: UUID4) -> Mapping:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post

# Dependency 2
async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}

# Dependency 3 uses both 1 & 2
async def valid_owned_post(
    post: Mapping = Depends(valid_post_id),
    token_data: dict = Depends(parse_jwt_data),
) -> Mapping:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()

    return post

# Dependency 4 also uses dependency 2 (and is cached)
async def valid_active_creator(
    token_data: dict = Depends(parse_jwt_data),
):
    user = await users_service.get_by_id(token_data["user_id"])
    if not user["is_active"]:
        raise UserIsBanned()

    if not user["is_creator"]:
       raise UserNotCreator()

    return user


# routes.py (uses both Dependency 3 & 4)
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(
    worker: BackgroundTasks,
    post: Mapping = Depends(valid_owned_post),
    user: Mapping = Depends(valid_active_creator),
):
    """Get post that belong the active user."""
    worker.add_task(notifications_service.send_email, user["id"])
    return post
```

###### Dependencies can include route parameters

- Sometimes a dependency requires additional variables to run it's logic.
- As an example we can imagine an app that has users and projects:
  - To determine if a user has permission to access a project we need both:
    - The user id
    - The project id
  - The user id could be determined via another dependency.
  - However, the project id must be passed in by the user.

```python
# logic.py (where dependencies are located)

from app.auth.osm import AuthUser, login_required # imported dependency

async def validator(
    project_id: int, # The route parameter
    db: Session = Depends(get_db),
    user_data: AuthUser = Depends(login_required), # from imported dependency
) -> AuthUser:
    user_id = await get_uid(user_data)

    match = (
        db.query(DbUserRoles).filter_by(user_id=user_id, project_id=project_id).first()
    )

    if not match:
        raise HTTPException(status_code=403, detail="User has no access to project")

    if match.role.value < ProjectRole.VALIDATOR.value:
        raise HTTPException(
            status_code=403, detail="User is not a validator for this project"
        )

    return user_data

# routes.py (endpoints)
@router.get("/get_validator/")
async def validator(
    db: Session = Depends(database.get_db),
    user: AuthUser = Depends(validator),
):
    return user
```

When the user calls the `/get_validator` endpoint, they will need to provide the
parameter `project_id`, as it is present in the `validator` sub dependency.

##### 5. Always Use Typing

- FastAPI relies on Typing heavily for it's functionality.
- Typing also helps linting and IDE code completion.

##### 6. Save Files in Chunks

- If the API needs to receive a large file from a user, receive it in chunks:

```python
import aiofiles
from fastapi import UploadFile

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50  # 50 megabytes

async def save_video(video_file: UploadFile):
   async with aiofiles.open("/file/path/name.mp4", "wb") as f:
     while chunk := await video_file.read(DEFAULT_CHUNK_SIZE):
         await f.write(chunk)
```
