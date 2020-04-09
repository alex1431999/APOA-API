"""
This class defines the parent test class for all tests
Every test shall inherit from this class
"""
import unittest

from server import app

class BaseTest(unittest.TestCase):
    def setUp(self):
        # context setup
        self.app_context = app.app_context()
        self.app_context.push()

        self.tester = app.test_client(self)

    def tearDown(self):
        self.app_context.pop()
