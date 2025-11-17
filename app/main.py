from fastapi import FastAPI, Depends, status, HTTPException
from .db import init_db, get_session
from . import crud, schemas
# https://github.com/ben519/todooo/blob/master/main.py
from sqlalchemy.orm import Session
import app.models as models
from typing import List

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operations with **tasks**.",
    },
    {
        "name": "Todo",
        "description": "Manage with _To Do_.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://github.com/SergeyMi37/fastapi-postges-docker-crud.git/",
        },
    },
]

app = FastAPI(
    title='Tasks and Todo Application',
    version='0.0.1',
    description="""
            Description async Todo & sync Tasks
                """,
    summary='Task and Todo',
    openapi_url="/api/v0/openapi.json",
    openapi_tags=tags_metadata
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/",summary='This just root',tags=['Todo','Tasks'])
def This_root():
    return "This root"

@app.get("/ping",description="Sent ping",response_description='txt_response_description',tags=['Todo','Tasks'])
async def pong():
    return {"ping": "pong!!!"}


@app.get("/todos",summary='Read all todos', response_model=list[schemas.Todo],tags=['Todo'])
async def read_todos(skip: int = 0, limit: int = 100, session=Depends(get_session)):
    todos = crud.get_todos(session, skip=skip, limit=limit)
    return todos


@app.post("/todos", response_model=schemas.Todo,tags=['Todo'])
async def create_todo(todo: schemas.TodoCreate, session=Depends(get_session)):
    return crud.create_todo(db=session, todo=todo)

@app.get("/todo/{id}", response_model=schemas.Todo,tags=['Todo'])
def read_todo(id: int, session: Session = Depends(get_session)):

    # get the Todo item with the given id
    todo = session.query(models.Todo).get(id)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.put("/todo/{id}", response_model=schemas.Todo,tags=['Todo'])
def update_todo(id: int, title: str,description: str, session: Session = Depends(get_session)):

    # get the task item with the given id
    t = session.query(models.Todo).get(id)

    # update task item with the given task (if an item with the given id was found)
    if t:
        t.title = title
        t.description = description
        session.commit()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not t:
        raise HTTPException(status_code=404, detail=f"task item with id {id} not found")

    return t

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=['Todo'])
def delete_todo(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.Todo).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None


# https://www.gormanalysis.com/blog/building-a-simple-crud-application-with-fastapi/
# https://github.com/ben519/todooo/blob/master/models.py

@app.get("/tasks", response_model = List[schemas.Tasks],tags=['Tasks'])
def read_tasks_list(session: Session = Depends(get_session)):

    # get all tasks items
    tasks_list = session.query(models.Tasks).all()

    return tasks_list

@app.post("/tasks", response_model=schemas.Tasks, status_code=status.HTTP_201_CREATED,tags=['Tasks'])
def create_task(tasks: schemas.TasksCreate, session: Session = Depends(get_session)):

    # create an instance of the ToDo database model
    taskdb = models.Tasks(task = tasks.task)

    # add it to the session and commit it
    session.add(taskdb)
    session.commit()
    session.refresh(taskdb)

    # return the task object
    return taskdb

@app.get("/task/{id}", response_model=schemas.Tasks,tags=['Tasks'])
def read_task(id: int, session: Session = Depends(get_session)):

    # get the Task item with the given id
    task = session.query(models.Tasks).get(id)

    # check if task item with given id exists. If not, raise exception and return 404 not found response
    if not task:
        raise HTTPException(status_code=404, detail=f"task item with id {id} not found")

    return task

@app.put("/task/{id}", response_model=schemas.Tasks,tags=['Tasks'])
def update_task(id: int, task: str, session: Session = Depends(get_session)):

    # get the task item with the given id
    t = session.query(models.Tasks).get(id)

    # update task item with the given task (if an item with the given id was found)
    if t:
        t.task = task
        session.commit()

    # check if task item with given id exists. If not, raise exception and return 404 not found response
    if not t:
        raise HTTPException(status_code=404, detail=f"task item with id {id} not found")

    return t

@app.delete("/task/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=['Tasks'])
def delete_task(id: int, session: Session = Depends(get_session)):

    # get the task item with the given id
    task = session.query(models.Tasks).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if task:
        session.delete(task)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"task item with id {id} not found")

    return None