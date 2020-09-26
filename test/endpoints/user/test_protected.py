"""
This file holds all protect endpoint tests
"""
from flask_jwt_extended import create_access_token

from test.base_test import BaseTest


class Test(BaseTest):
    def test_protected_unauthorized(self):
        response = self.tester.get("/protected")

        self.assertEqual(
            response.status_code,
            401,
            "Since there are no users, this should be rejected",
        )

    def test_protected_authorized(self):
        self.register_users()  # Register all users
        access_token = create_access_token(self.user_1["username"])
        headers = {"Authorization": f"Bearer {access_token}"}

        response = self.tester.get("/protected", headers=headers)

        self.assertEqual(response.status_code, 200, "Should have accepted the request")

    def test_protected_content(self):
        self.register_users()  # Register all users
        access_token = create_access_token(self.user_1["username"])
        headers = {"Authorization": f"Bearer {access_token}"}

        response = self.tester.get("/protected", headers=headers)
        response_data = response.get_json()

        self.assertIn(
            "logged_in_as",
            response_data,
            "The response should include the username currently logged in",
        )
        self.assertEqual(
            response_data["logged_in_as"],
            self.user_1["username"],
            "The username should match the user used",
        )
