"""
This file includes all tests for the get_keywords endpoint
"""
from flask_jwt_extended import create_access_token

from test.base_test import BaseTest

class Test(BaseTest):
    def setUp(self):
        super().setUp()
        self.register_users()

    def send_request(self, user, keyword):
        access_token = create_access_token(user['username'])
        headers = { 'Authorization': f'Bearer {access_token}' }
        response = self.tester.post('/keywords', headers=headers, json=keyword)

        return response

    def test_post_keywords(self):
        keyword = { 'keyword': 'test', 'language': 'en' }
        
        response = self.send_request(self.user_1, keyword)

        self.assertEqual(response.status_code, 200, 'The request should have been accepted')

