"""
This file holds all login endpoint tests
"""
from test.base_test import BaseTest


class Test(BaseTest):
    def test_login_unauthorized(self):
        body = self.user_1

        response = self.tester.post("/login", json=body)

        self.assertEqual(
            response.status_code,
            401,
            "Since no user is in the database the login should have failed",
        )

    def test_login_authorized(self):
        self.register_users()  # Register all users
        body = self.user_1

        response = self.tester.post("/login", json=body)

        self.assertEqual(
            response.status_code, 200, "Should have logged in successfully"
        )

    def test_login_content(self):
        self.register_users()  # Register all users
        body = self.user_1

        response = self.tester.post("/login", json=body)
        response_data = response.get_json()

        self.assertIn(
            "access_token", response_data, "The response should include an access token"
        )
        self.assertIn(
            "refresh_token",
            response_data,
            "The response should include a refresh token",
        )

        self.assertIsNotNone(
            response_data["access_token"], "The access token should have a value"
        )
        self.assertIsNotNone(
            response_data["refresh_token"], "The access token should have a value"
        )
