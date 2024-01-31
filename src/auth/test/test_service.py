import unittest
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from src.auth.service import AuthService
from src.main import app

client = TestClient(app=app)


class AuthServiceTest(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService()

    def test_create_access_token(self):
        # Testing with valid input data and default expiration time
        data = {"user_id": 123}
        token = self.auth_service.create_access_token(data=data)
        self.assertIsInstance(token, str)

        # Testing with valid input data and custom expiration time
        data = {"user_id": 456}
        token = self.auth_service.create_access_token(
            data=data, expires_delta=30)
        self.assertIsInstance(token, str)

    async def test_verify_password(self):
        # Testing with valid password
        hashed_password = "hashed_password"
        plain_password = "plain_password"
        self.assertTrue(await self.auth_service.verify_password(
            plain_password, hashed_password))

        # Testing with invalid password
        hashed_password = "hashed_password"
        plain_password = "invalid_password"
        self.assertFalse(await self.auth_service.verify_password(
            plain_password, hashed_password))


if __name__ == '__main__':
    unittest.main()
