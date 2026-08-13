import jwt
from src.models.api import ApiRequest, ApiResponse
from src.models.payloads.jwt import JwtPayload
from src.config import JWT_ALGO, settings
from datetime import datetime


def create_token(payload: ApiRequest[JwtPayload]) -> str:
    return jwt.encode({"email": payload.email, "role": payload.global_role.value, "exp": int(datetime.now().timestamp())}, settings.JWT_SIGNATURE, algorithm=JWT_ALGO)

def verify_token(jwtToken: str, payload: ApiRequest[JwtPayload], role: str = None) -> ApiResponse[dict]:
    if role is None:
        role = payload.global_role
    
    decodedToken = jwt.decode(jwtToken, settings.JWT_SIGNATURE, algorithms=[JWT_ALGO])

    if decodedToken['email'] != payload.email and decodedToken['role'] != payload.global_role:
        return ApiResponse(
                statusCode=401,
                message="Unauthorized",
                data={
                    "errorMessage": "jwtToken does not correspond to user email/role"
                }
            )

    if decodedToken['exp'] > datetime.now():
        return ApiResponse(
                statusCode=403,
                message="Forbidden",
                data={
                    "errorMessage": "jwtToken expired"
                }
            )

    if role != payload.global_role:
        return ApiResponse(
                statusCode=401,
                message="Unauthorized",
                data={
                    "errorMessage": "your role can't perform this operation"
                }
            )

    return ApiResponse(
        statusCode=200,
        message="successfully verified jwtTokens",
        data={
            "payload": payload,
            "jwtToken": jwtToken
        }
    )
    
    