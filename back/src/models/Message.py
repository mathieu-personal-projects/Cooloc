from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class Message():
    colocation_id: uuid4
    sender_id: uuid4
    content: str = ''
    created_at: datetime = datetime.now()