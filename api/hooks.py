"""
This file defines all the hooks used in the flask api
"""
import json

from bson import json_util
from flask import Response


def enable_hooks(app):
    @app.after_request
    def delete_user_sensitive_data(response: Response):
        """
        Remove sensitive user data from the response data
        """
        try:
            data = json.loads(response.data)
        except:
            return response

        data = remove_sensitive_data(data)

        response.data = json_util.dumps(data)
        return response

    @app.after_request
    def allow_cors(response: Response):
        """
        Allow access from anywhere
        """
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


def remove_sensitive_data(data: any) -> any:
    """
    Recursive function that will look through all elements
    within a nested list and dict structure and remove all
    sensitive data
    """
    if type(data) is list:
        for element in data:
            element = remove_sensitive_data(element)
    elif type(data) is dict:
        data = delete_user_sensitive_data_element(data)
    return data


def delete_user_sensitive_data_element(element: dict) -> dict:
    """
    Define all the fields that classify as user sensitive data
    """
    element = remove_field_save(element, "users")
    return element


def remove_field_save(element: dict, field: str) -> dict:
    """
    Remove a field from a dict if it is in the dict
    """
    if field in element:
        del element[field]
    return element
