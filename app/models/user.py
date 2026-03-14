from sqlalchemy import Column, String
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


# Base from app.db.base
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4 )

    auth0_id = Column(String, index=True, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=True)
