from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import login, predict, users
from app.core.config import settings
from app.routers import upload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOW_ORIGINS],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok 200"}


app.include_router(users.router)
app.include_router(login.router)
app.include_router(predict.router)
app.include_router(upload.router)
# app.include_router(upload.router)

# Base.metadata.create_all(bind=engine)
