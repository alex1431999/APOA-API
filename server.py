"""
This module holds the basic flask setup
"""
import os

from celery import Celery
from common.mongo.controller import MongoController
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from api.hooks import enable_hooks

# Construct mongo controller
MONGO_CONTROLLER = MongoController()

# Setup celery
celery_app = Celery("server", broker=os.environ["BROKER_URL"])

from api.endpoints.keyword import keyword_blueprint
from api.endpoints.user import user_blueprint
from api.endpoints.crawl import crawl_blueprint
from api.endpoints.static import static_blueprint

app = Flask(__name__, static_url_path="")

CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Set JWT secret key
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

# Enable JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(keyword_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(crawl_blueprint)
app.register_blueprint(static_blueprint)

enable_hooks(app)
