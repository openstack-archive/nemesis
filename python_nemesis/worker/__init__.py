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
import oslo_messaging
from python_nemesis.extensions import log
from python_nemesis.swift import download_from_swift


class NewFileEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        event_type='nemsis.new_file')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        file_uuid = payload['file_uuid']
        file_id = payload['file_id']
        log.logger.info("Fetched file_id %s to work on from the queue."
                        % file_id)

        log.logger.info("Downloading file from Swift for analysis.")
        download_from_swift(file_uuid)


def run_worker():
    cfg = current_app.config['cfg']
    transport = oslo_messaging.get_notification_transport(cfg)

    targets = [
        oslo_messaging.Target(topic='nemesis_notifications')
    ]
    endpoints = [
        NewFileEndpoint()
    ]

    pool = "nemesis_notifications.info"
    server = oslo_messaging.get_notification_listener(transport,
                                                      targets,
                                                      endpoints,
                                                      pool=pool)

    server.start()
    server.wait()
