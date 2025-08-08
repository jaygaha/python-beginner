import pytest
from datetime import timedelta
from src.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    hash_password,
    verify_password
)

def test_create_and_verify_access_token():
    """Test access token creation and verification"""
    user_id = "123"
    token = create_access_token(subject=user_id)
    assert token is not None

    verified_user_id = verify_token(token, token_type="access")
    assert verified_user_id == user_id

def test_create_and_verify_refresh_token():
    """Test refresh token creation and verification"""
    user_id = "123"
    token = create_refresh_token(subject=user_id)
    assert token is not None

    verified_user_id = verify_token(token, token_type="refresh")
    assert verified_user_id == user_id

def test_verify_invalid_token():
    """Test verification of invalid token"""
    invalid_token = "invalid.token.here"
    result = verify_token(invalid_token)
    assert result is None

def test_verify_wrong_token_type():
    """Test verification with wrong token type"""
    user_id = "123"
    access_token = create_access_token(subject=user_id)

    # Try to verify access token as refresh token
    result = verify_token(access_token, token_type="refresh")
    assert result is None

def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_token_expiration():
    """Test token with custom expiration"""
    user_id = "123"
    expires_delta = timedelta(minutes=1)
    token = create_access_token(subject=user_id, expires_delta=expires_delta)

    verified_user_id = verify_token(token)
    assert verified_user_id == user_id
