from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
import requests
from jose.exceptions import JWTError
from app.core.config import settings
from fastapi.security import OAuth2AuthorizationCodeBearer
#from fastapi_plugin.fast_api_client import Auth0FastAPI


# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl=f"https://{settings.AUTH0_DOMAIN}/authorize",
#     tokenUrl=f"https://{settings.AUTH0_DOMAIN}/oauth/token",
#     scopes={
#         "openid": "OpenID",
#         "profile": "Profile",
#         "email": "Email"
#     }
# )

security = HTTPBearer()

jwks = requests.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json").json()


def verify_token(token: str = Depends(security)):

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]

        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

        if key is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        payload = jwt.decode(
            token,
            key,
            algorithms=[settings.ALGORITHM],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
