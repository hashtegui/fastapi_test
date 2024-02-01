from unittest.mock import patch

from fastapi.testclient import TestClient

from src.domain.shared.users.model import User
from src.main import app

client = TestClient(app=app)


@patch('src.domain.shared.users.service.UserService.get_user_by_email')
@patch('src.auth.service.AuthService.verify_password')
def test_login_auth(mock_verify_password, mock_get_user_by_email):
    # Mock the user and password verification

    user = User(name="Test",
                email="test@example.com",
                password="password123", company_id=1)
    mock_get_user_by_email.return_value = user
    mock_verify_password.return_value = True

    # Send a request to the login endpoint

    response = client.post(
        "/api/auth/", data={
            "username": "test@example.com",
            "password": "password123"})

    # Assertions
    assert response.status_code == 200
    assert "email" in response.json()
    assert "access_token" in response.json()
    assert "permissions" in response.json()
