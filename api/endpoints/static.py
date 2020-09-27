"""
Any static files will be served from here
"""

from flask import Blueprint, send_file

# Set up blueprint
static_endpoint = Blueprint("static_endpoint", __name__)


@static_endpoint.route("/static/apoa/logo", methods=["GET"])
def get_apoa_logo():
    return send_file("assets/images/apoa/logo.svg")


@static_endpoint.route("/static/apoa/team/alex", methods=["GET"])
def get_apoa_team_alex():
    return send_file("assets/images/apoa/team/alex.jpg")


@static_endpoint.route("/static/apoa/team/anthony", methods=["GET"])
def get_apoa_team_anthony():
    return send_file("assets/images/apoa/team/anthony.jpg")


@static_endpoint.route("/static/isa/logo", methods=["GET"])
def get_isa_logo():
    return send_file("assets/images/isa/logo.svg")
