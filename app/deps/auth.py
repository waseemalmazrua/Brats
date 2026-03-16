from fastapi import Depends , HTTPException , status
from sqlalchemy.orm import Session

from app.core.security import auth
from app.db.session import get_db
from app.models.user import User
from app.core.security import veriy_token


def get_current_user(
    claims: dict = Depends(veriy_token()),
    db: Session = Depends(get_db),
):

    auth0_id = claims["sub"]

    if not auth0_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        

    user = db.query(User).filter(User.auth0_id == auth0_id).first()

    if not user:
        user = User(
            auth0_id=auth0_id,
            email=claims.get("email"),
            name=claims.get("name" , "User"),
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,detail="Could not create user"
            )

    return user
