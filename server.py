"""
This module holds the basic flask setup
"""
import os

from common.mongo.controller import MongoController
from flask_jwt_extended import JWTManager
from flask import Flask

# Construct mongo controller
MONGO_CONTROLLER = MongoController()

from api.enpoints.keyword import keyword_blueprint
from api.enpoints.user import user_blueprint

app = Flask(__name__)

# Set JWT secret key
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Enable JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(keyword_blueprint)
app.register_blueprint(user_blueprint)

