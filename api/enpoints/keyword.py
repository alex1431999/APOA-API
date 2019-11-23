"""
This module holds all the endpoints associated to keyword manipulation
"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

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
        pass
    elif request.method == 'POST':
        # Get transmitted parameters
        keyword = request.json.get('keyword', None)
        language = request.json.get('language', None)

        try:
            MONGO_CONTROLLER.add_keyword(keyword, language, username)
            return { 'msg': 'keyword successfully added' }, 200 # Successful
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad request

