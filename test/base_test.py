"""
This class defines the parent test class for all tests
Every test shall inherit from this class
"""
import unittest
import os

from common.mongo.controller import MongoController
from common.config import SUPPORTED_LANGUAGES
from datetime import datetime

from server import app


class BaseTest(unittest.TestCase):
    # Users
    user_1 = {"username": "user_1", "password": "test"}
    user_2 = {"username": "user_2", "password": "test"}

    # Crawls:News
    crawl_news_1 = {
        "author": "test",
        "title": "some title",
        "text": "some text",
        "timestamp": datetime.now(),
    }

    def setUp(self):
        # Mongo
        self.mongo_controller = MongoController()

        # context setup
        self.app_context = app.app_context()
        self.app_context.push()

        self.tester = app.test_client(self)

    def tearDown(self):
        self.app_context.pop()
        self.mongo_controller.client.drop_database(os.environ["MONGO_DATABASE_NAME"])

    def register_users(self):
        self.mongo_controller.add_user(self.user_1["username"], self.user_1["password"])
        self.mongo_controller.add_user(self.user_2["username"], self.user_2["password"])

    def load_keyword_fixture(self, user):
        keyword_string = "some keyword"
        language = SUPPORTED_LANGUAGES[0]

        self.mongo_controller.add_keyword(keyword_string, language, user["username"])
        keyword = self.mongo_controller.get_keyword(keyword_string, language)

        return keyword["_id"]

    def load_crawl_fixture(self, keyword_id):
        self.mongo_controller.add_crawl_news(
            keyword_id,
            self.crawl_news_1["author"],
            self.crawl_news_1["title"],
            self.crawl_news_1["text"],
            self.crawl_news_1["timestamp"],
        )

        crawl = self.mongo_controller.get_crawl_news(
            self.crawl_news_1["author"],
            self.crawl_news_1["title"],
        )

        return crawl["_id"]
