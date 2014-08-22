#!/usr/bin/env python

# Author: Will Stevens (CloudOps) - wstevens@cloudops.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Usage:
  api_examples.py (--host=<arg> --username=<arg> --password=<arg>) [options]
  api_examples.py (-h | --help)

Options:
  -h --help             Show this screen.
  --host=<arg>          NetScaler IP.
  --username=<arg>      NetScaler username.
  --password=<arg>      NetScaler password.
  --protocol=<arg>      Protocol used to connect to the NetScaler (http | https) [default: http].
  --base_path=<arg>     Base NetScaler API path [default: /nitro/v1].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log=<arg>           The log file to be used [default: logs/nitro_api.log].
  --clear_log=<arg>     Removes the log each time the API object is created [default: True].
"""

from docopt import docopt
from nitro_api import API
import pprint

args = docopt(__doc__)

if __name__ == '__main__':
    with API(args) as api:
        pprint.pprint(api.request('/stat/system'))