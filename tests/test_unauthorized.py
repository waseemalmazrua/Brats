from app.models.user import User


def test_get_me_unauthorized(client):
    response = client.get("/users/me")

    assert response.status_code == 401