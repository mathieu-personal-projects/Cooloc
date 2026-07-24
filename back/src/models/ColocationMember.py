from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from datetime import datetime


class RoomateRole(Enum):
    BASIC = "BASIC"
    LEAD = "LEAD"

@dataclass
class ColocationMember():
    colocation_id: uuid4
    user_id: uuid4
    role: RoomateRole = RoomateRole.BASIC
    joined_at: datetime = field(default_factory=datetime.now())