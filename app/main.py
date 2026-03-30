from fastapi import FastAPI
from app.routers import users
from app.routers import login
from app.routers import predict
from app.routers import upload
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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

# Base.metadata.create_all(bind=engine)
