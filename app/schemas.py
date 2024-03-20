from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str


class Todo(TodoCreate):
    id: int

    class Config:
        from_attributes = True

# Create Tasks Schema (Pydantic Model)
class TasksCreate(BaseModel):
    task: str

# Complete Tasks Schema (Pydantic Model)
class Tasks(BaseModel):
    id: int
    task: str

    class Config:
        orm_mode = True