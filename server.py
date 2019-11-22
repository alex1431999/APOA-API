"""
This module holds the basic flask setup
"""

from flask import Flask

from api.enpoints.keyword import keyword_blueprint

app = Flask(__name__)

# Register endpoints
app.register_blueprint(keyword_blueprint)
