from dataclasses import dataclass
from uuid import uuid4
from enum import Enum
from datetime import datetime


class ApplicationStatus(Enum):
    'PENDING'
    'ACCEPTED'
    'REJECTED'

@dataclass
class ColocationApplication():
    colocation_id: uuid4
    applicant_id: uuid4
    status: ApplicationStatus = 'PENDING'
    message: str
    created_at: datetime = datetime.now()