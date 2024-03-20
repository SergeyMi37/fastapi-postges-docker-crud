from fastapi import FastAPI, Depends, status
from .db import init_db, get_session
from . import crud, schemas

from sqlalchemy.orm import Session
import app.models as models

tags_metadata = [
    {
        "name": "Tag-1",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Tag-2",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title='TODO Application',
    version='0.0.1',
    description="  Description _Todo_ ",
    summary='Test',
    openapi_url="/api/v1/openapi.json",
    openapi_tags=tags_metadata
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/",summary='This just root',tags=['Tag-2'])
def This_root():
    return "This root"

@app.get("/ping",description="Sent ping",response_description='txt_response_description',tags=['Tag-1'])
async def pong():
    return {"ping": "pong!!!"}


@app.get("/todo",summary='Read all todos', response_model=list[schemas.Todo],tags=['Tag-2','Tag-1'])
async def read_todos(skip: int = 0, limit: int = 100, session=Depends(get_session)):
    todos = crud.get_todos(session, skip=skip, limit=limit)
    return todos


@app.post("/todo", response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, session=Depends(get_session)):
    return crud.create_todo(db=session, todo=todo)

"""
# https://www.gormanalysis.com/blog/building-a-simple-crud-application-with-fastapi/
# https://github.com/ben519/todooo/blob/master/models.py
@app.post("/todo_add", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo_new(todo: schemas.TodoCreate, session: Session = Depends(get_session)):

    # create an instance of the ToDo database model
    tododb = models.Todo(todo=todo)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    # return the todo object
    return tododb


@app.post("/todo", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):

    # create an instance of the ToDo database model
    tododb = models.ToDo(task = todo.task)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    # return the todo object
    return tododb

@app.get("/todo/{id}", response_model=schemas.ToDo)
def read_todo(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.ToDo).get(id)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.put("/todo/{id}", response_model=schemas.ToDo)
def update_todo(id: int, task: str, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.ToDo).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if todo:
        todo.task = task
        session.commit()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.ToDo).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None

@app.get("/todo", response_model = List[schemas.ToDo])
def read_todo_list(session: Session = Depends(get_session)):

    # get all todo items
    todo_list = session.query(models.ToDo).all()

    return todo_list
"""