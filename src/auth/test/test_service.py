import asyncio
from unittest.mock import patch

import pytest

from src.auth.service import AuthService


class TestAuthService:

    auth_service = AuthService()

    def test_create_access_token(self):
        # Testing with valid input data and default expiration time
        data = {"user_id": 123}
        token = self.auth_service.create_access_token(data=data)
        assert isinstance(token, str)

        # Testing with valid input data and custom expiration time
        data = {"user_id": 456}
        token = self.auth_service.create_access_token(
            data=data, expires_delta=30)
        assert isinstance(token, str)

    @pytest.mark.asyncio
    @patch("bcrypt.checkpw")
    async def test_verify_correct_password(self, mock_checkpw):
        # Arrange
        plain_password = "plain_password"
        hashed_password = "hashed_password"

        # Act
        await self.auth_service.verify_password(plain_password, hashed_password)

        # Assert
        mock_checkpw.assert_called_once_with(
            plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @patch('bcrypt.checkpw')
    @pytest.mark.asyncio
    async def test_verify_incorrect_password(self, mock_checkpw):
        # Arrange

        invalid_password = "invalid_password"
        hashed_password = "hashed_password"

        # Act
        await self.auth_service.verify_password(invalid_password, hashed_password)

        # Assert
        mock_checkpw.assert_called_once_with(
            invalid_password.encode('utf-8'), hashed_password.encode('utf-8'))
