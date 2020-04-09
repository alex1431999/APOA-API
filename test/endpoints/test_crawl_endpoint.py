"""
This file holds all crawl endpoint tests
"""
from bson import ObjectId

from test.base_test import BaseTest

class Test(BaseTest):
    def test_plotting_data_no_data(self):
        random_id = ObjectId
        response = self.tester.get(f'/crawls/{random_id}/plotting_data')

        self.assertEqual(response.status_code, 401, 'Request should have been rejected')
