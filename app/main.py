from fastapi import FastAPI
from app.routers import users
from app.routers import login

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok 200"}


app.include_router(users.router)
app.include_router(login.router)


# Base.metadata.create_all(bind=engine)
