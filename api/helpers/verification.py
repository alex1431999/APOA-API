"""
This module handles custom verification methods unrelated to JWT
"""
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

from server import MONGO_CONTROLLER


def verify_keyword_association(id_parameter_name):
    """
    Verify that a user is associated to a keyword they are trying to request

    :param str id_parameter_name: The name of the _id parameter
    """

    def verify_keyword_association_inner(func):
        """
        The inner wrapper of the decorator

        :param func func: The function which holds the to be verified parameters
        """

        @jwt_required
        def verify(*args, **kwargs):
            username = get_jwt_identity()

            if id_parameter_name in kwargs:  # Make sure the dict actually has this key
                _id = kwargs[id_parameter_name]
                keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, username=username)
                if keyword:
                    return func(*args, **kwargs)

            # If the above did not pass then the user is not authorized
            return jsonify("You are not authorized to access this keyword"), 404

        verify.__name__ = (
            func.__name__
        )  # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
        return verify

    return verify_keyword_association_inner
