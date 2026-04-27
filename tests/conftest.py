import pytest
from unittest.mock import patch, MagicMock

# ✅ mock أول شي قبل أي import من app
with patch("requests.get", return_value=MagicMock(json=lambda: {"keys": []})):
    from app.core.security import verify_token
    from app.main import app

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://test:test@localhost:5436/test_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def get_db_override():
        yield db
    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


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