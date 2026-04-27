import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import verify_token
from app.db.base import Base
from app.db.session import get_db
from app.main import app
import os
# ------------------------------------------------------------



# tests/conftest.py

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://test:test@localhost:5436/test_db"  # fallback محلي
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


# ---------------------------------------------
@pytest.fixture
def client(db):

    def get_db_override():
        yield db

    app.dependency_overrides[get_db] = get_db_override

    client = TestClient(app)

    yield client 

    app.dependency_overrides.clear()



    #------------------------------------------------


@pytest.fixture
def override_auth():
    def fake_verify_token():
        return {
            "sub": "auth0|123",
            "email_verified": True,
            "https://brats.app/email": "test@test.com",
            "https://brats.app/name": "Waseem",
        }

 
    app.dependency_overrides[verify_token] = fake_verify_token

    yield

    app.dependency_overrides.clear()