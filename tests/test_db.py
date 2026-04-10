from app.models.user import User

def test_get_me_creates_user(client, db, override_auth):

    response = client.get("/users/me")

    assert response.status_code == 200

    data = response.json()

 
    assert data["email"] == "test@test.com"
    assert data["name"] == "Waseem"

   
    user = db.query(User).filter(User.auth0_id == "auth0|123").first()

    assert user is not None