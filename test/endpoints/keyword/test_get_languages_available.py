"""
This file includes all tests for the available languages endpoint
"""
from flask_jwt_extended import create_access_token
from common.config import SUPPORTED_LANGUAGES

from test.base_test import BaseTest


class Test(BaseTest):
    def setUp(self):
        super().setUp()
        self.register_users()

    def send_request(self, user):
        access_token = create_access_token(user["username"])
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.tester.get("/keywords/languages/available", headers=headers)

        return response

    def test_languages_available_content(self):
        response = self.send_request(self.user_1)

        self.assertEqual(response.status_code, 200, "Should have been authorized")

        response_data = response.get_json()

        self.assertEqual(
            response_data,
            SUPPORTED_LANGUAGES,
            "The langauges returned should equal the ones in the common library",
        )
