from pydantic import BaseModel, EmailStr
from src.models.User import UserGlobalRole


class UserRegisterPayload(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
    global_role: UserGlobalRole = UserGlobalRole.APPLICANT