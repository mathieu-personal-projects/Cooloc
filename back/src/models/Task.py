from dataclasses import dataclass, field
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
    description: str
    title: str = "Dummy Task"
    status: TaskStatus = TaskStatus.TODO
    due_date: datetime = field(default_factory=datetime.now())
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())