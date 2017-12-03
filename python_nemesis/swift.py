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

from flask import current_app
import os
import swiftclient.client as swiftclient


def upload_to_swift(filename, file_id):
    config = current_app.config['cfg']
    auth_version = config.swift.auth_version
    swift_session = swiftclient.Connection(authurl=config.swift.auth_uri,
                                           user=config.swift.user,
                                           key=config.swift.password,
                                           tenant_name=config.swift.project,
                                           auth_version=auth_version)

    with open(os.path.join(filename), 'rb') as upload_file:
        container = config.swift.container.encode('utf-8')
        file_id = str(file_id).encode('utf-8')
        swift_session.put_object(container, file_id, upload_file)
