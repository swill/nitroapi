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
  cli_example.py [--json=<arg>] [--endpoint=<arg> --username=<arg> --password=<arg>] [options]
  cli_example.py (-h | --help)

Options:
  -h --help             Show this screen.
  --json=<arg>          Path to a JSON config file with the same names as the options (without the '--' prefix).
  --endpoint=<arg>      NetScaler URL.
  --username=<arg>      NetScaler username.
  --password=<arg>      NetScaler password.
  --base_path=<arg>     Base NetScaler API path [default: /nitro/v1].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log_level=<arg>     The logging verbosity. [default: DEBUG].
                        Valid entries are: CRITICAL | ERROR | WARNING | INFO | DEBUG | NOTSET
  --log=<arg>           The log file to be used [default: logs/nitroapi.log].
  --clear_log=<arg>     Removes the log each time the API object is created [default: True].
  --verify_ssl=<arg>    Verify the SSL Certificate for a target HTTPS endpoint [default: True].
"""

from nitroapi import CLI
import pprint

if __name__ == '__main__':
    # call the constructor with the __doc__ value...
    with CLI(__doc__) as api:
        pprint.pprint(api.request('/stat/system'))