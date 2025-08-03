import unittest
from datetime import timedelta
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import ValidationError
import jwt
import hashlib
from src.dependencies import (
    DatabaseConnection, get_database, create_access_token, verify_token,
    get_current_user, get_admin_user, PaginationParams, SortingParams,
    RateLimiter, check_rate_limit, validate_positive_int, get_item_id,
    CommonQueryParams, users_db, SECRET_KEY, ALGORITHM, User, rate_limiter
)

class TestDependencies(unittest.TestCase):

    def setUp(self):
        self.valid_token = create_access_token({"sub": "admin"})
        self.invalid_token = "invalid.token.here"
        # Use the global rate_limiter for tests involving check_rate_limit
        self.rate_limiter = rate_limiter

    def tearDown(self):
        # Clean up any test users added
        users_db.pop("inactive", None)

    def test_database_connection(self):
        db = DatabaseConnection()
        self.assertTrue(db.connected)
        self.assertTrue(db.connection_id.startswith("conn_"))
        db.close()
        self.assertFalse(db.connected)

    def test_get_database(self):
        db_gen = get_database()
        db = next(db_gen)
        self.assertTrue(db.connected)
        db_gen.close()
        self.assertFalse(db.connected)

    def test_create_access_token(self):
        data = {"sub": "admin"}
        token = create_access_token(data, expires_delta=timedelta(minutes=30))
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], "admin")
        self.assertIn("exp", decoded)

    def test_verify_token_valid(self):
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=self.valid_token)
        username = verify_token(credentials)
        self.assertEqual(username, "admin")

    def test_verify_token_invalid(self):
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=self.invalid_token)
        with self.assertRaises(HTTPException) as cm:
            verify_token(credentials)
        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(cm.exception.detail, "Could not validate credentials")

    def test_get_current_user_valid(self):
        user = get_current_user(username="admin")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.roles, ["admin", "user"])
        self.assertTrue(user.is_active)

    def test_get_current_user_nonexistent(self):
        with self.assertRaises(HTTPException) as cm:
            get_current_user(username="nonexistent")
        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(cm.exception.detail, "User not found")

    def test_get_current_user_inactive(self):
        users_db["inactive"] = {
            "id": 3,
            "username": "inactive",
            "email": "inactive@example.com",
            "hashed_password": hashlib.sha256("pass123".encode()).hexdigest(),
            "roles": ["user"],
            "is_active": False
        }
        with self.assertRaises(HTTPException) as cm:
            get_current_user(username="inactive")
        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.detail, "Inactive user")

    def test_get_admin_user_valid(self):
        user = User(id=1, username="admin", email="admin@example.com", roles=["admin", "user"], is_active=True)
        admin_user = get_admin_user(user)
        self.assertEqual(admin_user.username, "admin")

    def test_get_admin_user_non_admin(self):
        user = User(id=2, username="jay", email="jay@example.com", roles=["user"], is_active=True)
        with self.assertRaises(HTTPException) as cm:
            get_admin_user(user)
        self.assertEqual(cm.exception.status_code, 403)
        self.assertEqual(cm.exception.detail, "Not enough permissions")

    def test_pagination_params_valid(self):
        params = PaginationParams(skip=5, limit=20)
        self.assertEqual(params.skip, 5)
        self.assertEqual(params.limit, 20)

    def test_sorting_params_valid(self):
        params = SortingParams(sort_by="name", sort_order="desc")
        self.assertEqual(params.sort_by, "name")
        self.assertEqual(params.sort_order, "desc")


    def test_rate_limit_allowed(self):
        client_ip = "127.0.0.1"
        result = self.rate_limiter.is_allowed(client_ip, limit=2, window=3600)
        self.assertTrue(result)
        result = self.rate_limiter.is_allowed(client_ip, limit=2, window=3600)
        self.assertTrue(result)

    def test_rate_limit_exceeded(self):
        client_ip = "127.0.0.1"
        self.rate_limiter.is_allowed(client_ip, limit=2, window=3600)
        self.rate_limiter.is_allowed(client_ip, limit=2, window=3600)
        result = self.rate_limiter.is_allowed(client_ip, limit=2, window=3600)
        self.assertFalse(result)

    def test_check_rate_limit(self):
        client_ip = check_rate_limit(x_forwarded_for="192.168.1.1")
        self.assertEqual(client_ip, "192.168.1.1")

    def test_check_rate_limit_exceeded(self):
        client_ip = "192.168.1.2"
        # Exhaust the global rate limiter for this IP
        for _ in range(100):
            self.rate_limiter.is_allowed(client_ip, limit=100, window=3600)
        with self.assertRaises(HTTPException) as cm:
            check_rate_limit(x_forwarded_for=client_ip)
        self.assertEqual(cm.exception.status_code, 429)
        self.assertEqual(cm.exception.detail, "Rate limit exceeded")

    def test_validate_positive_int_valid(self):
        result = validate_positive_int(42)
        self.assertEqual(result, 42)

    def test_validate_positive_int_invalid(self):
        with self.assertRaises(HTTPException) as cm:
            validate_positive_int(0)
        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.detail, "Value must be positive")

    def test_get_item_id(self):
        item_id = get_item_id(10)
        self.assertEqual(item_id, 10)

    def test_common_query_params_valid(self):
        params = CommonQueryParams(q="test", include_inactive=True)
        self.assertEqual(params.q, "test")
        self.assertTrue(params.include_inactive)


if __name__ == '__main__':
    unittest.main()
