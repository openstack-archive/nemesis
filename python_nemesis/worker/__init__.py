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
import oslo_messaging
from python_nemesis.db.utilities import update_status_by_file_id
from python_nemesis.extensions import log
from python_nemesis.swift import delete_from_swift
from python_nemesis.swift import download_from_swift
from python_nemesis.worker_app import create_worker_app


class NewFileEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        event_type='nemsis.new_file')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        with create_worker_app().app_context():
            file_uuid = payload['file_uuid']
            file_id = payload['file_id']

            container = CONF.swift.container.encode('utf-8')
            log.logger.info("Fetched file_id %s to work on from the queue."
                            % file_id)

            log.logger.info("Downloading file from Swift for analysis.")
            download_from_swift(container, file_uuid)
            log.logger.info("Fetched file to /tmp/%s" % file_uuid)

            log.logger.info("Running analysis plugins.")
            log.logger.info("Updating file analysis ")

            log.logger.info("Cleaning up analysis subject.")
            delete_from_swift('incoming_files', file_uuid)

            log.logger.info("Setting file status to complete.")
            update_status_by_file_id(file_id, 'complete')


def run_worker():
    transport = oslo_messaging.get_notification_transport(CONF)

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
                                                      executor='threading',
                                                      pool=pool)

    server.start()
    server.wait()
