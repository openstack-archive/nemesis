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

from python_nemesis.extensions import db


class Files(db.Model):
    __tablename__ = 'file'
    file_id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    sha512_hash = db.Column(db.UnicodeText(), nullable=True, index=True)
    sha256_hash = db.Column(db.UnicodeText(), nullable=True, index=True)
    sha1_hash = db.Column(db.UnicodeText(), nullable=True, index=True)
    md5_hash = db.Column(db.UnicodeText(), nullable=True, index=True)
    size = db.Column(db.Float(), nullable=True)
    mime_type = db.Column(db.String(40), nullable=True)
    submitted_by = db.Column(db.String(120), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    first_seen = db.Column(db.DateTime, nullable=False)
    file_lookup = db.relationship("FileLookupRequest")

    def to_dict(self):
        return {"sha512": self.sha512_hash,
                "sha256": self.sha256_hash,
                "sha1": self.sha1_hash,
                "md5": self.md5_hash,
                "size": self.size,
                "mime_type": self.mime_type,
                "status": self.status,
                "last_updated": self.last_updated,
                "first_seen": self.first_seen}


class FileLookupRequest(db.Model):
    __tablename__ = 'lookup_request'
    request_id = db.Column(db.BigInteger(), primary_key=True,
                           autoincrement=True)
    requested_at = db.Column(db.DateTime, nullable=False)
    requestor = db.Column(db.String(120), nullable=False)
    file_id = db.Column(db.ForeignKey(Files.file_id), nullable=True)
    lookup_hash = db.Column(db.UnicodeText(), nullable=False)
    result = db.Column(db.String(20), nullable=False)
