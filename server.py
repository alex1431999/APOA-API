"""
This module holds the basic flask setup
"""
import os

from common.mongo.controller import MongoController
from flask_jwt_extended import JWTManager
from celery import Celery
from flask import Flask
from flask_cors import CORS

# Construct mongo controller
MONGO_CONTROLLER = MongoController()

# Setup celery
celery_app = Celery('server',
    broker = os.environ['BROKER_URL']
)

from api.enpoints.keyword import keyword_blueprint
from api.enpoints.user import user_blueprint
from api.enpoints.crawl import crawl_enpoint

app = Flask(__name__)

CORS(app)

# Set JWT secret key
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Enable JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(keyword_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(crawl_enpoint)

