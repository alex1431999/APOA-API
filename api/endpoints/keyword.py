"""
This module holds all the endpoints associated to keyword manipulation

By giving each individual request its own controller we establish individual
connections which prevents the connection from getting overloaded.
"""
import json
import sys

from bson import json_util
from common.celery import queues
from common.config import SUPPORTED_LANGUAGES
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from api.helpers.verification import verify_keyword_association
from server import MONGO_CONTROLLER, celery_app

# Set up blueprint
keyword_blueprint = Blueprint("keyword_endpoint", __name__)


@keyword_blueprint.route("/keywords", methods=["GET", "POST"])
@jwt_required
def keywords_route():
    """
    Handle all requests on /keywords

    GET: Get all keywords of a user
    POST: Add keyword
    """
    username = get_jwt_identity()

    # Get all keywords
    if request.method == "GET":
        try:
            # Get keywords from DB
            keywords = MONGO_CONTROLLER.get_keywords_user(username)

            # Serialize ID by casting to string
            keywords = json_util.dumps(keywords)

            # Load back into JSON format
            keywords = json.loads(keywords)

            return jsonify(keywords), 200  # Return keywords
        except:
            return {"msg": "the request encountered an error"}, 400  # Bad request

    # Add keyword
    elif request.method == "POST":
        # Get transmitted parameters
        keyword_string = request.json.get("keyword", None)
        language = request.json.get("language", None)

        try:
            keyword = MONGO_CONTROLLER.add_keyword(
                keyword_string, language, username, return_object=True
            )

            if keyword_string and language:
                celery_app.send_task(
                    "crawl-twitter-keyword",
                    kwargs={"keyword_string": keyword_string, "language": language},
                    queue=queues["twitter"],
                )
                celery_app.send_task(
                    "crawl-news-keyword",
                    kwargs={"keyword_string": keyword_string, "language": language},
                    queue=queues["news"],
                )
                celery_app.send_task(
                    "crawl-nyt-keyword",
                    kwargs={"keyword_string": keyword_string, "language": language},
                    queue=queues["nyt"],
                )

            return json_util.dumps(keyword), 200  # Successful
        except:
            return {"msg": "the request encountered an error"}, 400  # Bad request


@keyword_blueprint.route("/keywords/<_id>", methods=["GET", "DELETE"])
@verify_keyword_association(id_parameter_name="_id")
@jwt_required
def keyword_route(_id):
    """
    Hanlde all requests on /keywords/<_id>

    GET: get a specific keyword
    DELETE: delete a specific keyword
    """
    username = get_jwt_identity()

    # Delete keyword
    if request.method == "DELETE":
        try:
            MONGO_CONTROLLER.delete_keyword(_id, username)

            return {"msg": "keyword successfully deleted"}, 200  # Successful
        except:
            return {"msg": "the request encountered an error"}, 400  # Bad reqeust

    # Get specific keyword
    if request.method == "GET":
        try:
            # We don't need to verify that the user is authorized to access the keyword
            # the verify_keyword_association decorator handles that
            keyword = MONGO_CONTROLLER.get_keyword_by_id(_id)

            return json_util.dumps(keyword)  # Successful
        except:
            return {"msg": "the request encountered an error"}, 400  # Bad reqeust


@keyword_blueprint.route("/keywords/<_id>/score", methods=["GET"])
@jwt_required
@verify_keyword_association(id_parameter_name="_id")
def keyword_avg_score_route(_id):
    """
    Get the average score of a keyword

    GET: avg score
    """
    try:
        avg = MONGO_CONTROLLER.get_crawls_average_score(_id)

        return jsonify(avg)
    except:
        return {"msg": "the request encountered an error"}, 400  # Bad reqeust


@keyword_blueprint.route("/keywords/languages/available", methods=["GET"])
@jwt_required
def keyword_languages_available_route():
    """
    Return the currently supported languages of the system

    GET: supported languages
    """
    if request.method == "GET":
        return jsonify(SUPPORTED_LANGUAGES)


@keyword_blueprint.route("/keywords/<_id>/graph/entities", methods=["GET"])
@jwt_required
@verify_keyword_association(id_parameter_name="_id")
def keyword_graph_entities(_id):
    """
    Gather all entities of a keyword and their connections

    :param ObjectId _id: The id of the keyword which entities are requested
    """
    username = get_jwt_identity()

    limit = request.args.get("limit", sys.maxsize)

    keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, cast=True)

    entities = MONGO_CONTROLLER.get_entities(keyword._id, int(limit))

    return jsonify(entities)


@keyword_blueprint.route("/keywords/<_id>/graph/categories", methods=["GET"])
@jwt_required
@verify_keyword_association(id_parameter_name="_id")
def keyword_graph_categories(_id):
    """
    Gather all categories of a keyword and their connections

    :param ObjectId _id: The id of the keyword which categories are requested
    """
    username = get_jwt_identity()

    limit = request.args.get("limit", sys.maxsize)

    keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, cast=True)

    categories = MONGO_CONTROLLER.get_categories(keyword._id, int(limit))

    return jsonify(categories)


@keyword_blueprint.route("/keywords/<_id>/snippets", methods=["GET"])
@jwt_required
@verify_keyword_association(id_parameter_name="_id")
def keyword_snippets(_id):
    snippets = MONGO_CONTROLLER.get_crawls_texts(_id)
    return jsonify(snippets)


@keyword_blueprint.route("/keywords/public", methods=["GET"])
def keywords_public_endpoint():
    keywords = MONGO_CONTROLLER.get_keywords_public()
    return json_util.dumps(keywords)
