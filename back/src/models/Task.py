from dataclasses import dataclass
from uuid import uuid4
from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

@dataclass
class Task():
    colocation_id: uuid4
    assigned_to_id: uuid4
    title: str = "Dummy Task"
    description: str
    status: TaskStatus = TaskStatus.TODO
    due_date: datetime = datetime.now()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()