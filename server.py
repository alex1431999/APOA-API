"""
This module holds the basic flask setup
"""

from common.mongo.controller import MongoController
from flask import Flask

from api.enpoints.keyword import keyword_blueprint

app = Flask(__name__)

# Register endpoints
app.register_blueprint(keyword_blueprint)

# Construct mongo controller
MONGO_CONTROLLER = MongoController()
