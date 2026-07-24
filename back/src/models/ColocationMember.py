from dataclasses import dataclass
from uuid import uuid4
from enum import Enum
from datetime import datetime


class RoomateRole(Enum):
    'BASIC'
    'LEAD'

@dataclass
class ColocationMember():
    colocation_id: uuid4
    user_id: uuid4
    role: RoomateRole = 'BASIC'
    joined_at: datetime = datetime.now()