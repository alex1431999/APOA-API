"""
This file holds all refresh endpoint tests
"""
from flask_jwt_extended import create_refresh_token

from test.base_test import BaseTest


class Test(BaseTest):
    def test_refresh_unauthorized(self):
        response = self.tester.post("/refresh")

        self.assertEqual(
            response.status_code,
            401,
            "Since there are no users, this should be rejected",
        )

    def test_refresh_authorized(self):
        self.register_users()  # Register all users
        refresh_token = create_refresh_token(self.user_1["username"])
        headers = {"Authorization": f"Bearer {refresh_token}"}

        response = self.tester.post("/refresh", headers=headers)

        self.assertEqual(
            response.status_code, 200, "Should have refreshed the access token"
        )

    def test_refresh_content(self):
        self.register_users()  # Register all users
        refresh_token = create_refresh_token(self.user_1["username"])
        headers = {"Authorization": f"Bearer {refresh_token}"}

        response = self.tester.post("/refresh", headers=headers)
        response_data = response.get_json()

        self.assertIn(
            "access_token",
            response_data,
            "The response should have sent back a new access_token",
        )
        self.assertIsNotNone(
            response_data["access_token"], "The access token should have a value"
        )
