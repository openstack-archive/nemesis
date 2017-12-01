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
from flask_keystone import current_user
from python_nemesis.db.models import FileLookupRequest
from python_nemesis.db.models import Files
from python_nemesis.extensions import db
from sqlalchemy import or_


def add_request(lookup_hash, result, file_id=None):
    now = datetime.datetime.now()
    nreq = FileLookupRequest(requested_at=now,
                             requestor=current_user.user_id,
                             file_id=file_id,
                             lookup_hash=lookup_hash,
                             result=result)
    db.session.add(nreq)
    db.session.commit()


def search_by_hash(lookup_hash):
    results = db.session.query(Files). \
        filter(or_(Files.sha512_hash == lookup_hash,
                   Files.sha256_hash == lookup_hash,
                   Files.sha1_hash == lookup_hash,
                   Files.md5_hash == lookup_hash,
                   Files.crc32 == lookup_hash))

    ret_results = []
    for file in results:
        ret_results.append(file.to_dict())

    return ret_results
