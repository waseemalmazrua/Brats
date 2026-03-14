from fastapi import FastAPI
from app.routers import users
from app.db.base import Base
from app.db.session import engine

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok 200"}


app.include_router(users.router)


# Base.metadata.create_all(bind=engine)
