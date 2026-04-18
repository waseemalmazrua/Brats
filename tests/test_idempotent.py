
from app.models.user import User


def test_get_me_idempotent(client, db, override_auth):
    client.get("/users/me")
    client.get("/users/me")

    users = db.query(User).filter(User.auth0_id == "auth0|123").all()

    assert len(users) == 1