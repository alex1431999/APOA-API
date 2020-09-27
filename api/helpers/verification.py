"""
This module handles custom verification methods unrelated to JWT
"""
from flask_jwt_extended import get_jwt_identity, jwt_required

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

                # Check if the keyword is associated directly
                keyword = MONGO_CONTROLLER.get_keyword_by_id(_id, cast=True)
                if not keyword:
                    return {"msg": "The keyword you are trying to access does not exist"}, 404

                if username in keyword.users:
                    return func(*args, **kwargs)

                # Check if the keyword is associated indirectly by index
                indexes = [MONGO_CONTROLLER.get_index_by_id(_id, cast=True) for _id in keyword.indexes]
                indexes_users = []
                for index in indexes:
                    if index:
                        indexes_users += index.users

                if username in indexes_users:
                    return func(*args, **kwargs)

                # This is an edge case, we don't combine the if statements because these are mongo calls that take time
                keywords_public = MONGO_CONTROLLER.get_keywords_public()
                keywords_public_ids = [
                    str(keyword["_id"]) for keyword in keywords_public
                ]

                if _id in keywords_public_ids:
                    return func(*args, **kwargs)

            # If the above did not pass then the user is not authorized
            return {"msg": "You are not authorized to access this keyword"}, 401

        verify.__name__ = (
            func.__name__
        )  # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
        return verify

    return verify_keyword_association_inner
