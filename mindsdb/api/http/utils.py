import json
import os

from flask import Response


def http_error(status_code, detail=None, type=None):
    """
    Returns an HTTP error compliant with RFC 7807.
    """
    response = {
        "status": status_code,
    }
    if type:
        response["type"] = type
    if detail:
        response["detail"] = detail
    return make_response(jsonify(response), status_code)
    
@app.errorhandler(400)
def handle_bad_request(e):
    return http_error(400, "Bad request")

@app.errorhandler(401)
def handle_unauthorized(e):
    return http_error(401, "Unauthorized")

@app.errorhandler(404)
def handle_not_found(e):
    return http_error(404, "Resource not found")


def __is_within_directory(directory, target):
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    prefix = os.path.commonprefix([abs_directory, abs_target])
    return prefix == abs_directory


def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not __is_within_directory(path, member_path):
            raise Exception("Attempted Path Traversal in Tar File")
    tar.extractall(path, members, numeric_owner)
