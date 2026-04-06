import requests
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings

security = HTTPBearer()

# جلب مفاتيح Auth0 (JWKS)
JWKS_URL = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
jwks = requests.get(JWKS_URL).json()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
       
        token = credentials.credentials

        # قراءة الهيدر بدون تحقق
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token header")

        # نجيب المفتاح الصحيح من JWKS
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

        if key is None:
            raise HTTPException(status_code=401, detail="Public key not found")

        #  فك التوكن والتحقق منه
        payload = jwt.decode(
            token,
            key,
            algorithms=[settings.ALGORITHM],  
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )

        return payload

    except JWTError as e:
        print(f"JWT error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        print(f"Token error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")