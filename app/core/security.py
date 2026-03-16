from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
import requests

from app.core.config import settings


security = HTTPBearer()


jwks = requests.get(
    f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
).json()


def veriy_token(token=Depends(security)):

    try:
        payload = jwt.decode(
            token.credentials,
            jwks,
            algorithms=[settings.ALGORITHM],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )

        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")