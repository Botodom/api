# Homework models

from pydantic import BaseModel

class Homework(BaseModel):
    title: str
    deadline: str
    subject: str
    description: str
    notifications: bool
    completed: bool
