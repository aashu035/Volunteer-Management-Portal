"""Unit tests for security module — password hashing and JWT tokens."""

import asyncio
import pytest
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        """Test that hashed password can be verified."""
        hashed = asyncio.get_event_loop().run_until_complete(hash_password("MyPass@123"))
        assert hashed != "MyPass@123"
        result = asyncio.get_event_loop().run_until_complete(verify_password("MyPass@123", hashed))
        assert result is True

    def test_wrong_password_fails(self):
        """Test that wrong password fails verification."""
        hashed = asyncio.get_event_loop().run_until_complete(hash_password("MyPass@123"))
        result = asyncio.get_event_loop().run_until_complete(verify_password("WrongPass", hashed))
        assert result is False


class TestJWT:
    def test_create_and_decode_access_token(self):
        """Test access token creation and decoding."""
        data = {"sub": "test-user-id", "role": "admin"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "test-user-id"
        assert payload["role"] == "admin"
        assert payload["type"] == "access"

    def test_create_and_decode_refresh_token(self):
        """Test refresh token creation and decoding."""
        data = {"sub": "test-user-id", "role": "volunteer"}
        token = create_refresh_token(data)
        payload = decode_token(token)
        assert payload is not None
        assert payload["type"] == "refresh"

    def test_invalid_token_returns_none(self):
        """Test that invalid token decoding returns None."""
        assert decode_token("invalid.token.string") is None

    def test_tokens_have_unique_jti(self):
        """Test that each token has a unique JTI."""
        data = {"sub": "test-user-id"}
        t1 = create_access_token(data)
        t2 = create_access_token(data)
        p1 = decode_token(t1)
        p2 = decode_token(t2)
        assert p1["jti"] != p2["jti"]
