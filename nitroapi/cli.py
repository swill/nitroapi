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

import docopt
import json
import sys
from .nitroapi import API

class CLI(API):
    """
    Login and run queries against the Nitro API for NetScaler 10.x+.

    ## Recommended usage using WITH (to automatically login and logout):
    with CLI(__doc__) as api:
        pprint.pprint(api.request('/stat/system'))

    ## Manual setup and tear down example (requires explicit logout):
    api = CLI(__doc__)
    api.request('/config/login', {
        'login': {
            'username':api.username,
            'password':api.password
        }
    })
    system_stats = api.request('/stat/system')
    api.request('/config/logout', {'logout': {}})
    """
    def __init__(self, doc_str):
        args = self.load_config(doc_str)

        username = args['--username']
        password = args['--password']
        endpoint = args['--endpoint']
        base_path = args['--base_path']
        logging = True if args['--logging'].lower() == 'true' else False
        log_level = args['--log_level'].upper()
        log = args['--log']
        clear_log = True if args['--clear_log'].lower() == 'true' else False
        verify_ssl = True if args['--verify_ssl'].lower() == 'true' else False

        super(CLI, self).__init__(
            username,
            password,
            endpoint,
            base_path,
            logging,
            log_level,
            log,
            clear_log,
            verify_ssl
        )


    def load_config(self, doc_str):
        args = docopt.docopt(doc_str)

        is_set = [
            x.split('=')[0] \
            for x in sys.argv[1:] \
            if len(x.split('=')) > 0 and x.split('=')[0].startswith('-')
        ] # set by cmd line

        config = None
        if '--json' in args and args['--json']:
            with open(args['--json']) as json_config:
                config = json.load(json_config)

        if config:
            for key, value in config.iteritems():
                if '--%s' % (key) not in is_set:
                    args['--%s' % (key)] = value
        return args
