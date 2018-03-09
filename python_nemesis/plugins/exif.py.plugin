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

import exifread


class NemesisPlugin(object):
    plugin_name = 'Exif'

    def __init__(self, file_data):
        self.file_data = file_data

    def analyse(self):
        exif_formats = ['image/jpeg', 'image/tiff']
        file_type = self.file_data['file_type']
        if file_type in exif_formats:
            tags = self._extract_exif_tags()
            result = {"success": True,
                      "result": {'exif_tags': tags},
                      "message": None}
            return result

        else:
            result = {"success": False,
                      "result": None,
                      "message": ("File format %s is not an EXIF compatible "
                                  "format such as JPEG or TIFF, unable to "
                                  "perform EXIF extraction." % file_type)}
            return result

    def _extract_exif_tags(self):
        with open('/tmp/%s' % self.file_data['file_uuid'], 'rb') as f:
            tags = exifread.process_file(f)

        ret_tags = {}
        for k, v in tags.items():
            try:
                ret_tags[k] = v.printable
            except AttributeError:
                ret_tags[k] = str(v)
        return ret_tags
