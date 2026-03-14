from auth0_fastapi_api import Auth0FastAPI # type: ignore
from app.core.config import settings


# Initialize the Auth0 validator
# It automatically handles token extraction and signature verification
auth = Auth0FastAPI(
    domain=settings.AUTH0_AUDIENCE,
    audience=settings.AUTH0_AUDIENCE

)
