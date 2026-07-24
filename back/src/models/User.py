from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class UserGlobalRole(Enum):
    APPLICANT = "APPLICANT"
    ROOMMATE = "ROOMMATE"
    OWNER = "OWNER"

@dataclass
class User():
    password_hash: str
    phone_number: str
    email: str = "dummy@dum.com"
    first_name: str = "Dummy"
    last_name: str = "Dummy"
    global_role: UserGlobalRole = UserGlobalRole.APPLICANT
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())