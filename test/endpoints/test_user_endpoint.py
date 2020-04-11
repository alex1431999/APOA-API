"""
This file holds all user endpoint tests
"""
from flask_jwt_extended import create_access_token, create_refresh_token

from test.base_test import BaseTest

class Test(BaseTest):
    def test_login_unauthorized(self):
        body = self.user_1
        
        response = self.tester.post('/login', json=body)

        self.assertEqual(response.status_code, 401, 'Since no user is in the database the login should have failed')

    def test_login_authorized(self):
        self.register_users() # Register all users
        body = self.user_1
        
        response = self.tester.post('/login', json=body)

        self.assertEqual(response.status_code, 200, 'Should have logged in successfully')

    def test_login_content(self):
        self.register_users() # Register all users
        body = self.user_1
        
        response = self.tester.post('/login', json=body)
        response_data = response.get_json()

        self.assertIn('access_token', response_data, 'The response should include an access token')
        self.assertIn('refresh_token', response_data, 'The response should include a refresh token')

        self.assertIsNotNone(response_data['access_token'], 'The access token should have a value')
        self.assertIsNotNone(response_data['refresh_token'], 'The access token should have a value')

    def test_refresh_unauthorized(self):
        response = self.tester.post('/refresh')

        self.assertEqual(response.status_code, 401, 'Since there are no users, this should be rejected')

    def test_refresh_authorized(self):
        self.register_users() # Register all users
        refresh_token = create_refresh_token(self.user_1['username'])
        headers = { 'Authorization': f'Bearer {refresh_token}' }

        response = self.tester.post('/refresh', headers=headers)

        self.assertEqual(response.status_code, 200, 'Should have refreshed the access token')

    def test_refresh_content(self):
        self.register_users() # Register all users
        refresh_token = create_refresh_token(self.user_1['username'])
        headers = { 'Authorization': f'Bearer {refresh_token}' }

        response = self.tester.post('/refresh', headers=headers)
        response_data = response.get_json()

        self.assertIn('access_token', response_data, 'The response should have sent back a new access_token')
        self.assertIsNotNone(response_data['access_token'], 'The access token should have a value')

    def test_protected_unauthorized(self):
        response = self.tester.get('/protected')

        self.assertEqual(response.status_code, 401, 'Since there are no users, this should be rejected')

    def test_protected_authorized(self):
        self.register_users() # Register all users
        access_token = create_access_token(self.user_1['username'])
        headers = { 'Authorization': f'Bearer {access_token}' }

        response = self.tester.get('/protected', headers=headers)

        self.assertEqual(response.status_code, 200, 'Should have accepted the request')

    def test_protected_content(self):
        self.register_users() # Register all users
        access_token = create_access_token(self.user_1['username'])
        headers = { 'Authorization': f'Bearer {access_token}' }

        response = self.tester.get('/protected', headers=headers)
        response_data = response.get_json()

        self.assertIn('logged_in_as', response_data, 'The response should include the username currently logged in')
        self.assertEqual(response_data['logged_in_as'], self.user_1['username'], 'The username should match the user used')
