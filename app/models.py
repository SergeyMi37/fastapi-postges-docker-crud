from sqlalchemy import Column, Integer, String, Text
from app.db import Base


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=False)

# Define Tasks class inheriting from Base
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))