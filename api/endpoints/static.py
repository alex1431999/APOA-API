"""
Any static files will be served from here
"""

from flask import Blueprint, send_file

# Set up blueprint
static_blueprint = Blueprint("static_blueprint", __name__)


@static_blueprint.route("/static/apoa/logo", methods=["GET"])
def get_apoa_logo():
    return send_file("assets/images/apoa/logo.svg")


@static_blueprint.route("/static/apoa/team/alex", methods=["GET"])
def get_apoa_team_alex():
    return send_file("assets/images/apoa/team/alex.jpg")


@static_blueprint.route("/static/apoa/team/anthony", methods=["GET"])
def get_apoa_team_anthony():
    return send_file("assets/images/apoa/team/anthony.jpg")


@static_blueprint.route("/static/isa/logo", methods=["GET"])
def get_isa_logo():
    return send_file("assets/images/isa/logo.svg")
