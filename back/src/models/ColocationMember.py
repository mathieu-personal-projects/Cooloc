from dataclasses import dataclass
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
    joined_at: datetime = datetime.now()