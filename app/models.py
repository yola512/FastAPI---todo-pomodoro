from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

# input validation
# base Task model to create and update tasks
class TaskBase(BaseModel):
    id: Optional[int] # automatically generated in app logic
    title: str = Field(..., min_length=3, max_length=100) # required jeszcze unique w logice apki (np czy tyutl istnieje w liscie zadan)!!
    description: Optional[str] = Field(None, max_length=300)
    status: Literal["TODO", "IN_PROGRESS", "DONE"] = "TODO" # default: "TODO"; automatically validating status (can be 1 one of those 3)

# Task model to read task data (with id)
class Task(TaskBase):
    id: int

# Pomodoro model
class Pomodoro(BaseModel):
    task_id: int
    start_time: datetime
    end_time: datetime
    completed: bool

