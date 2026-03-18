from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_token
from uuid import uuid4


def get_current_user(
    claims: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):

    auth0_id = claims.get("sub")

    if not auth0_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    email_verified = claims.get("email_verified")
    if email_verified is not email_verified and not None:
        raise HTTPException(status_code=403, detail="Email not verified")

    user = db.query(User).filter(User.auth0_id == auth0_id).first()

    if not user:
        user = User(
            id=str(uuid4()),
            auth0_id=auth0_id,
            email=claims.get("https://brats.app/email"),
            name=claims.get("https://brats.app/name"),
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=500, detail="Could not create user")

    return user
