"""
This file includes all tests for the get keyword by id endpoint
"""
from flask_jwt_extended import create_access_token
from bson import ObjectId

from test.base_test import BaseTest


class Test(BaseTest):
    def setUp(self):
        super().setUp()
        self.register_users()

    def send_request(self, user, _id):
        access_token = create_access_token(user["username"])
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.tester.get(f"/keywords/{str(_id)}", headers=headers)

        return response

    def test_get_keywords_id_unauthorized(self):
        random_id = ObjectId()

        response = self.send_request(self.user_1, random_id)

        self.assertEqual(response.status_code, 400, "Should have not been authorized")

    def test_get_keywords_id_authorized(self):
        keyword_id = self.load_keyword_fixture(self.user_1)

        response = self.send_request(self.user_1, keyword_id)

        self.assertEqual(response.status_code, 200, "Should have been authorized")
