"""
This module holds all the endpoints associated to keyword manipulation
"""
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, jsonify
from bson import json_util

import json

from server import MONGO_CONTROLLER

# Set up blueprint
keyword_blueprint = Blueprint('keyword_endpoint', __name__)

@keyword_blueprint.route('/keywords', methods=['GET', 'POST'])
@jwt_required
def keywords_route():
    """
    Handle all requests on /keywords

    GET: Get all keywords of a user
    POST: Add keyword
    """
    username = get_jwt_identity()

    if request.method == 'GET':
        try:
            # Get keywords from DB
            keywords = MONGO_CONTROLLER.get_keywords_user(username)

            # Serialize ID by casting to string
            keywords = json_util.dumps(keywords)

            # Load back into JSON format
            keywords = json.loads(keywords)
            
            return jsonify(keywords), 200 # Return keywords
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad request
    elif request.method == 'POST':
        # Get transmitted parameters
        keyword = request.json.get('keyword', None)
        language = request.json.get('language', None)

        try:
            # Add keyword
            MONGO_CONTROLLER.add_keyword(keyword, language, username)

            return { 'msg': 'keyword successfully added' }, 200 # Successful
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad request

