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

from oslo_config.cfg import CONF
import os
import swiftclient.client as swiftclient


def upload_to_swift(filename, file_id):
    auth_version = CONF.swift.auth_version
    swift_session = swiftclient.Connection(authurl=CONF.swift.auth_uri,
                                           user=CONF.swift.user,
                                           key=CONF.swift.password,
                                           tenant_name=CONF.swift.project,
                                           auth_version=auth_version)

    with open(os.path.join(filename), 'rb') as upload_file:
        container = CONF.swift.container.encode('utf-8')
        file_id = str(file_id).encode('utf-8')
        swift_session.put_object(container, file_id, upload_file)


def download_from_swift(file_uuid):
    auth_version = CONF.swift.auth_version
    swift_session = swiftclient.Connection(authurl=CONF.swift.auth_uri,
                                           user=CONF.swift.user,
                                           key=CONF.swift.password,
                                           tenant_name=CONF.swift.project,
                                           auth_version=auth_version)

    container = CONF.swift.container.encode('utf-8')
    obj = swift_session.get_object(container, file_uuid)
    with open('/tmp/%s' % file_uuid, 'wb') as download_file:
        download_file.write(obj[1])
