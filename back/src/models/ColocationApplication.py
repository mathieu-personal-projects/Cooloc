from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from datetime import datetime


class ApplicationStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

@dataclass
class ColocationApplication():
    colocation_id: uuid4
    applicant_id: uuid4
    message: str
    status: ApplicationStatus = ApplicationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now())