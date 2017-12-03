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


def submit_worker_notification(msg):
    config = current_app.config['cfg']
    transport = oslo_messaging.get_notification_transport(config)
    notifier = oslo_messaging.Notifier(transport,
                                       'nemesis.api',
                                       driver='messagingv2',
                                       topics=['nemesis_notifications'])
    notifier.info({}, 'nemsis.new_file', msg)
