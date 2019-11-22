"""
This module holds all the endpoints associated to keyword manipulation
"""

from flask import Blueprint, request
from common.mongo.controller import MongoController

# Set up blueprint
keyword_blueprint = Blueprint('keyword_endpoint', __name__)

# Set up mongo controller
mongo_controller = MongoController()

@keyword_blueprint.route('/keywords', methods=['GET', 'POST'])
def keywords_route():
    """
    Handle all requests on /keywords

    GET: Get all keywords of a user
    POST: Add keyword
    """
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        # Get transmitted parameters
        keyword = request.json.get('keyword', None)
        language = request.json.get('language', None)

        try:
            mongo_controller.add_keyword(keyword, language)
            return { 'msg': 'keyword successfully added' }, 200 # Successful
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad request

