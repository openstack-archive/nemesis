# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from flask import request
import json
from python_nemesis.extensions import log


def general_handler(error):
    log.logger.exception("Hit exception during %s" % request)

    try:
        status_code = error.status_code
        ret_data = json.dumps(error.to_dict())
    except Exception:
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

    def __init__(self, message, title=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if title:
            self.title = title
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.status_code
        rv['title'] = self.title
        rv['message'] = self.message
        return rv


class NotFoundException(NemesisException):
    status_code = 404
    title = "Not Found"
    message = ""
