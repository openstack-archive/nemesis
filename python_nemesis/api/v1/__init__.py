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

from flask import Blueprint
from flask import jsonify
from python_nemesis.exceptions import general_handler
from python_nemesis.exceptions import NemesisException
from python_nemesis.exceptions import NotFoundException
from python_nemesis.extensions import log
from python_nemesis.db.utilities import add_request
from python_nemesis.db.utilities import search_by_hash


V1_API = Blueprint('v1_api', __name__)


@V1_API.errorhandler(NemesisException)
def handle_exception(error):
    return general_handler(error)


@V1_API.route('/v1')
def api_definition():
    return ""


@V1_API.route('/v1/file/<string:req_hash>')
def lookup_hash(req_hash):
    try:
        result = search_by_hash(req_hash)
    except Exception as err:
        log.logger.error(str(err))
        raise NemesisException(str(err))

    if len(result) == 0:
        add_request(req_hash, 'not_found')
        raise NotFoundException("Unable to find file with hash %s." % req_hash)

    elif len(result) == 1:
        add_request(req_hash, 'found', file_id=result[0]['file_id'])

    else:
        add_request(req_hash, 'multiple_found')

    return jsonify(result)


@V1_API.route('/v1/file', methods=['POST'])
def post_file():
    return ""
