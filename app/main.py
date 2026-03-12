from fastapi import FastAPI
from app.routers import users

app =  FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok 200"}

app.include_router(users.router)
