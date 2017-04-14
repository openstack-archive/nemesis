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
from python_nemesis.exceptions import general_handler
from python_nemesis.exceptions import NemesisException


V1_API = Blueprint('v1_api', __name__)


@V1_API.errorhandler(NemesisException)
def handle_exception(error):
    return general_handler(error)


@V1_API.route('/v1')
def api_definition():
    return ""
