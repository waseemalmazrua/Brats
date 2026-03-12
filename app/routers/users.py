from fastapi import APIRouter , Depends
from app.core.security import auth

router = APIRouter(
    prefix="/users",
    tags=["users"])

@router.get("/me")
def login(claims : dict = Depends(auth.require_auth())):
    return claims

