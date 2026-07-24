from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime


@dataclass
class Message():
    colocation_id: uuid4
    sender_id: uuid4
    content: str = 'dummy'
    created_at: datetime = field(default_factory=datetime.now())