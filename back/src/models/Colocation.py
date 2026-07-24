from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class Colocation():
    owner_id: uuid4
    title: str = "Dummy"
    description: str = "Dummy"
    address: str = "Dummy address"
    city: str = "DummyCity"
    postal_code: int = "12345"
    rent_amount: float = 10.4
    max_capacity: int = 0
    is_available: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()