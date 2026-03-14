from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import auth
from app.db.session import get_db
from app.models.user import User


def get_current_user(
    claims: dict = Depends(auth.require_auth()),
    db: Session = Depends(get_db),
):

    auth0_id = claims["sub"]

    user = db.query(User).filter(User.auth0_id == auth0_id).first()

    if not user:
        user = User(
            auth0_id=auth0_id,
            email=claims.get("email"),
            name=claims.get("name"),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    return user
