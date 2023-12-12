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

##### Using Synchronous Code

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

#### Note

- If you regularly find you are running out of workers/threads and the
  server is overloaded, it may be time to add a task queuing system to your stack.
- Celery is made for just this - defer tasks to a queue, and run gradually
  to reduce the immediate load.
