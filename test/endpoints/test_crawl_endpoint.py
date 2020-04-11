"""
This file holds all crawl endpoint tests
"""
from flask_jwt_extended import create_access_token
from bson import ObjectId
from datetime import datetime

from test.base_test import BaseTest

class Test(BaseTest):
    def setUp(self):
        super().setUp()

        # Register all users for these tests
        self.register_users()

    def send_request(self, keyword_id, user):
        access_token = create_access_token(user['username'])
        headers = { 'Authorization': f'Bearer {access_token}' }

        return self.tester.get(f'/crawls/{keyword_id}/plotting_data', headers=headers)

    def test_plotting_data_no_keyword(self):
        random_id = ObjectId()
        response = self.send_request(random_id, self.user_1)

        self.assertEqual(response.status_code, 401, 'Request should have been rejected')

    def test_plotting_data_invalid_user(self):
        keyword_id = self.load_keyword_fixture(self.user_1)

        response = self.send_request(keyword_id, self.user_2)

        self.assertEqual(response.status_code, 401, 'Request should have been rejected')

    def test_plotting_data_no_data(self):
        keyword_id = self.load_keyword_fixture(self.user_1)

        response = self.send_request(keyword_id, self.user_1)
        response_data = response.get_json()

        self.assertEqual(response_data, [], 'Since there is no plotting data, an empty list should be returned')

    def test_plotting_data_with_data(self):
        keyword_id = self.load_keyword_fixture(self.user_1)
        timestamp = datetime.now().isoformat()
        text = 'some text'
        score = 15

        tweet = self.mongo_controller.add_crawl_twitter(keyword_id, 123, 'some text', 15, 15, timestamp, return_object=True)
        tweet = self.mongo_controller.set_score_crawl(tweet['_id'], score, return_object=True)

        response = self.send_request(keyword_id, self.user_1)
        response_data = response.get_json()

        plotting_data_expected = [{ 'score': score, 'text': text, 'timestamp': timestamp}]
        self.assertEqual(response_data, plotting_data_expected)

