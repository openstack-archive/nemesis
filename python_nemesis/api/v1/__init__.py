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

import datetime
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_keystone import current_user
import os
from python_nemesis.db.utilities import add_request
from python_nemesis.db.utilities import create_new_file
from python_nemesis.db.utilities import get_file_by_sha512_hash
from python_nemesis.db.utilities import search_by_hash
from python_nemesis.exceptions import general_handler
from python_nemesis.exceptions import NemesisException
from python_nemesis.exceptions import NotFoundException
from python_nemesis.extensions import db
from python_nemesis.extensions import log
from python_nemesis.file_hasher import get_all_hashes
import uuid
from werkzeug.utils import secure_filename


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
    filename = secure_filename(str(uuid.uuid4()))
    filename = '/tmp/%s' % filename
    file = request.files['file']

    if 'Content-Range' in request.headers:
        # extract starting byte from Content-Range header string
        range_str = request.headers['Content-Range']
        start_bytes = int(range_str.split(' ')[1].split('-')[0])

        # append chunk to the file on disk, or create new
        with open(filename, 'a') as f:
            f.seek(start_bytes)
            f.write(file.stream.read())

    else:
        # this is not a chunked request, so just save the whole file
        file.save(filename)

    file_hashes = get_all_hashes(filename)
    current_file = get_file_by_sha512_hash(file_hashes['sha512'])
    file_size = os.path.getsize(filename)

    if current_file:
        file_id = current_file.file_id
        current_file.last_updated = datetime.datetime.now()
        current_file.status = 'analysing'
        db.session.commit()
        file_dict = current_file.to_dict()

    else:
        file = create_new_file(file_hashes['md5'],
                               file_hashes['sha1'],
                               file_hashes['sha256'],
                               file_hashes['sha512'],
                               file_size,
                               current_user.user_id)
        file_id = file.file_id
        file_dict = file.to_dict()

    return jsonify(file_dict)
