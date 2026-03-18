from fastapi import APIRouter

router = APIRouter()


@router.get("/callback")
def callback():
    return {"message": "Login successful"}
