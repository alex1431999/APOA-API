"""
This module holds all the endpoints associated to crawl result access
"""

from flask import Blueprint, request, jsonify

from api.helpers.verification import verify_keyword_association
from server import MONGO_CONTROLLER

# Set up blueprint
crawl_enpoint = Blueprint("crawl_endpoint", __name__)


@crawl_enpoint.route("/crawls/<keyword_id>/plotting_data", methods=["GET"])
@verify_keyword_association(id_parameter_name="keyword_id")
def plotting_data_route(keyword_id):
    if request.method == "GET":
        try:
            plotting_data = MONGO_CONTROLLER.get_crawls_plotting_data(keyword_id)
            return jsonify(plotting_data)
        except:
            return {"msg": "the request encountered an error"}, 400  # Bad reqeust
