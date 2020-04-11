"""
This file includes all tests for the get_keywords endpoint
"""
from flask_jwt_extended import create_access_token

from test.base_test import BaseTest

class Test(BaseTest):
    def setUp(self):
        super().setUp()
        self.register_users()

    def send_request(self, user):
        access_token = create_access_token(user['username'])
        headers = { 'Authorization': f'Bearer {access_token}' }
        response = self.tester.get('/keywords', headers=headers)

        return response

    def test_get_keywords_no_keywords(self):
        response = self.send_request(self.user_1)

        self.assertEqual(response.status_code, 200, 'The request should have been accepted')

        expected_data = []
        response_data = response.get_json()

        self.assertEqual(response_data, expected_data, 'The data returned should match what was expected')

    def test_get_keywords_with_keywords(self):
        keyword_id = self.load_keyword_fixture(self.user_1)

        response = self.send_request(self.user_1)
        response_data = response.get_json()

        self.assertEqual(len(response_data), 1, 'Should have returned one keyword')
        self.assertEqual(response_data[0]['_id']['$oid'], str(keyword_id), 'The returned keyword should match the one inserted')

    def test_get_keywords_wrong_user(self):
        self.load_keyword_fixture(self.user_1) # Only user 1 has keywords

        response = self.send_request(self.user_2) # But we are requesting keywords using user 2

        self.assertEqual(response.status_code, 200, 'The request should still be valid')

        expected_data = [] # User 2 should have 0 keywords
        response_data = response.get_json()

        self.assertEqual(expected_data, response_data, 'The data returned should match what was expected')
