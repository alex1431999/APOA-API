"""
Athentication
(https://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html)
"""

from flask import request, Blueprint, jsonify

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
)

from server import MONGO_CONTROLLER

user_blueprint = Blueprint("user_endpoint", __name__)


@user_blueprint.route("/login", methods=["POST"])
def login():
    """
    Login a user and create tokens which are then returned
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    try:  # If except isnt called then the customer must have been found
        user = MONGO_CONTROLLER.get_user(username)

        if not user.verifiy(password):
            raise Exception("Password didnt verify")

        ret = {
            "access_token": create_access_token(identity=username),
            "refresh_token": create_refresh_token(identity=username),
        }

        # return ret with status code 200
        return jsonify(ret), 200
    except Exception as ex:
        print(ex)
        return jsonify({"msg": "Bad username or password"}), 401


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@user_blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    ret = {"access_token": create_access_token(identity=current_user)}
    return jsonify(ret), 200


@user_blueprint.route("/protected", methods=["GET"])
@jwt_required
def protected():
    """
    Used to confirm that a user is still logged in.
    :returns username
    """
    username = get_jwt_identity()

    return jsonify(logged_in_as=username), 200
