"""
This file includes all tests for get keyword avg score endpoint
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
        response = self.tester.get(f"/keywords/{str(_id)}/score", headers=headers)

        return response

    def test_get_keyword_avg_score_unauthorized(self):
        random_id = ObjectId()

        response = self.send_request(self.user_1, random_id)

        self.assertEqual(
            response.status_code,
            404,
            "The user should have not been authorized get the avg score of the keyword",
        )

    def test_get_keyword_avg_score_authorized(self):
        keyword_id = self.load_keyword_fixture(self.user_1)

        response = self.send_request(self.user_1, keyword_id)

        self.assertEqual(response.status_code, 200, "Should have been authorized")

    def test_get_keyword_avg_score_content(self):
        score = 5
        keyword_id = self.load_keyword_fixture(self.user_1)
        crawl_id = self.load_crawl_fixture(keyword_id)
        self.mongo_controller.set_score_crawl(crawl_id, score)

        response = self.send_request(self.user_1, keyword_id)

        self.assertEqual(response.status_code, 200, "Should have been authorized")

        response_data = response.get_json()

        self.assertEqual(
            response_data, score, "The avg score should equal the expected score"
        )
