"""
Any static files will be served from here
"""

from flask import Blueprint, send_file

# Set up blueprint
static_endpoint = Blueprint("static_endpoint", __name__)


@static_endpoint.route("/static/apoa/logo", methods=["GET"])
def get_apoa_logo():
    return send_file("assets/images/apoa/logo.svg")


@static_endpoint.route("/static/isa/logo", methods=["GET"])
def get_isa_logo():
    return send_file("assets/images/isa/logo.svg")