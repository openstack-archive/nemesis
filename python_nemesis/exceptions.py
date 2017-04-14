import json
from flask import request
from python_nemesis.extensions import log


def general_handler(error):
    log.logger.exception("Hit exception during %s" % request)

    try:
        status_code = error.status_code
        ret_data = json.dumps(error.to_dict())
    except:
        status_code = 500
        ret_data = {"title": "Internal Server Error",
                    "code": status_code,
                    "message": ""}
        ret_data = json.dumps(ret_data)

    return ret_data, status_code


class NemesisException(Exception):
    status_code = 500
    title = "Internal Server Error"
    message = ""

    def __init__(self, title, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.title = title
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.status_code
        rv['title'] = self.title
        rv['message'] = self.message
        return rv
