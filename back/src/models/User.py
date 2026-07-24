from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class UserGlobalRole(Enum):
    APPLICANT = "APPLICANT"
    ROOMMATE = "ROOMMATE"
    OWNER = "OWNER"

@dataclass
class User():
    email: str = "dummy@dum.com"
    password_hash: str
    first_name: str = "Dummy"
    last_name: str = "Dummy"
    phone_number: str
    global_role: UserGlobalRole = UserGlobalRole.APPLICANT
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()