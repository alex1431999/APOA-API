"""
This module holds all the endpoints associated to crawl result access
"""

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, jsonify

from server import MONGO_CONTROLLER

# Set up blueprint
crawl_enpoint = Blueprint("crawl_endpoint", __name__)


@crawl_enpoint.route("/crawls/<keyword_id>/plotting_data", methods=["GET"])
@jwt_required
def plotting_data_route(keyword_id):
    user = get_jwt_identity()

    # Verify user
    try:
        keyword = MONGO_CONTROLLER.get_keyword_by_id(keyword_id, user, cast=True)
        assert user in keyword.users
    except:
        return {
            "msg": "the user is not authorized to view this data"
        }, 401  # Not authorized

    if request.method == "GET":
        try:
            plotting_data = MONGO_CONTROLLER.get_crawls_plotting_data(keyword_id)
            return jsonify(plotting_data)
        except:
            return {"msg": "the request encountered an error"}, 400  # Bad reqeust
