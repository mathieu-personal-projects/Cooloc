from pydantic import BaseModel, EmailStr
from src.models.User import UserGlobalRole


class JwtPayload(BaseModel):
    email: EmailStr
    global_role: UserGlobalRole = UserGlobalRole.APPLICANT