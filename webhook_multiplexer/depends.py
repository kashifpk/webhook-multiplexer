from fastapi import Request, status
from fastapi.exceptions import HTTPException
from .config import get_settings


def authenticated_request(request: Request) -> None:
    settings = get_settings()
    auth_token = request.headers.get('authorization', '')

    if auth_token != settings.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
