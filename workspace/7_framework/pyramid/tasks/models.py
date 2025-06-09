from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class Task(Base):
    """
    SQLAlchemy model for a task.

    Attributes:
        id: Unique identifier for the task.
        title: Short title of the task.
        description: Detailed description of the task.
        completed: Boolean indicating whether the task is completed.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Task(title='{self.title}')>"
