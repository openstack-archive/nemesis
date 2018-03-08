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

from python_nemesis.base_app import configure_app
from python_nemesis.base_app import configure_extensions
from python_nemesis.base_app import create_app


def create_worker_app():
    app = create_app('nemesis-worker')
    configure_app(app)
    configure_extensions(app)
    return app


if __name__ == "__main__":  # pragma: no cover
    from python_nemesis.worker import run_worker
    app = create_worker_app()
    with app.app_context():
        run_worker()
