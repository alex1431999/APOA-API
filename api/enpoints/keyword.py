"""
This module holds all the endpoints associated to keyword manipulation

A global Mongo Controller is used while a local individual Neo controller
is used for each function which requires a neo controller. 

The reason behind that is that Mongo can handle multiple concurrent queries
while neo seems to struggle with multile queries sent over one connection.

By giving each individual request its own controller we establish individual
connections which prevents the connection from getting overloaded.
"""
import json

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, jsonify
from bson import json_util
from common.celery import queues
from common.config import SUPPORTED_LANGUAGES
from common.neo4j.controller import Neo4jController

from server import MONGO_CONTROLLER, celery_app
from api.helpers.verification import verify_keyword_association

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

    # Get all keywords
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

    # Add keyword
    elif request.method == 'POST':
        # Get transmitted parameters
        keyword_string = request.json.get('keyword', None)
        language = request.json.get('language', None)

        try:
            MONGO_CONTROLLER.add_keyword(keyword_string, language, username)

            if keyword_string and language:
                celery_app.send_task('crawl-twitter-keyword', kwargs={'keyword_string': keyword_string, 'language': language}, queue=queues['twitter'])
                celery_app.send_task('crawl-news-keyword', kwargs={'keyword_string': keyword_string, 'language': language}, queue=queues['news'])
                celery_app.send_task('crawl-nyt-keyword', kwargs={'keyword_string': keyword_string, 'language': language}, queue=queues['nyt'])

            return { 'msg': 'keyword successfully added' }, 200 # Successful
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad request

@keyword_blueprint.route('/keywords/<_id>', methods=['GET', 'DELETE'])
@jwt_required
def keyword_route(_id):
    """
    Hanlde all requests on /keywords/<_id>

    GET: get a specific keyword
    DELETE: delete a specific keyword
    """
    username = get_jwt_identity()

    # Delete keyword
    if request.method == 'DELETE':
        try:
            MONGO_CONTROLLER.delete_keyword(_id, username)

            return { 'msg': 'keyword successfully deleted' }, 200 # Successful
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad reqeust

    # Get specific keyword
    if request.method == 'GET':
        try:
            keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, username)

            # You don't want to publish any information about other users
            del keyword['users']

            return json_util.dumps(keyword) # Successful
        except:
            return { 'msg': 'the request encountered an error' }, 400 # Bad reqeust

@keyword_blueprint.route('/keywords/<_id>/score', methods=['GET'])
@jwt_required
@verify_keyword_association(id_parameter_name='_id')
def keyword_avg_score_route(_id):
    """
    Get the average score of a keyword

    GET: avg score
    """
    try:
        avg = MONGO_CONTROLLER.get_crawls_average_score(_id)

        return jsonify(avg)
    except:
        return { 'msg': 'the request encountered an error' }, 400 # Bad reqeust


@keyword_blueprint.route('/keywords/languages/available', methods=['GET'])
@jwt_required
def keyword_languages_available_route():
    """
    Return the currently supported languages of the system

    GET: supported languages
    """
    if request.method == 'GET':
        return jsonify(SUPPORTED_LANGUAGES)

@keyword_blueprint.route('/keywords/<_id>/graph/entities', methods=['GET'])
@jwt_required
@verify_keyword_association(id_parameter_name='_id')
def keyword_graph_entities(_id):
    """
    Gather all entities of a keyword and their connections

    :param ObjectId _id: The id of the keyword which entities are requested
    """
    neo_controller = Neo4jController()

    username = get_jwt_identity()

    entity_limit = request.args.get('limit', neo_controller.MAX_32_INT)

    keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, username=username, cast=True)

    results = neo_controller.get_keyword_entities(keyword, entity_limit=entity_limit)

    results = [result.data() for result in results]

    results = [{ 'keyword': result['kw']._properties, 'entity': result['en']._properties, 'mentionedWith': result['mw']._properties } for result in results]

    return jsonify(results)

@keyword_blueprint.route('/keywords/<_id>/graph/categories', methods=['GET'])
@jwt_required
@verify_keyword_association(id_parameter_name='_id')
def keyword_graph_categories(_id):
    """
    Gather all categories of a keyword and their connections

    :param ObjectId _id: The id of the keyword which categories are requested
    """
    neo_controller = Neo4jController()

    username = get_jwt_identity()

    category_limit = request.args.get('limit', neo_controller.MAX_32_INT)

    keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, username=username, cast=True)

    results = neo_controller.get_keyword_categories(keyword, category_limit=category_limit)

    results = [result.data() for result in results]

    results = [{ 'keyword': result['kw']._properties, 'category': result['ca']._properties, 'mentionedWith': result['mw']._properties } for result in results]

    return jsonify(results)
            

@keyword_blueprint.route('/keywords/<_id>/snippets', methods=['GET'])
@jwt_required
@verify_keyword_association(id_parameter_name='_id')
def keyword_snippets(_id):
    snippets = MONGO_CONTROLLER.get_crawls_texts(_id)
    return jsonify(snippets)
