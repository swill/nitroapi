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
  nitro_api.py (--host=<arg> --username=<arg> --password=<arg>) [options]
  nitro_api.py (-h | --help)

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
import json
import os
import pprint
import requests
import urlparse
import urllib

args = docopt(__doc__)

class API(object):
    """
    Login and run queries against the Nitro API for NetScaler 10.1.

    ## Recommended usage using WITH (to automatically login and logout):
    with API(args) as api:
        system_stats = api.request('/stat/system')

    ## Manual setup and tear down example (requires explicit logout):
    api = API(args)
    api.request('/config/login', {
        'login': {
            'username':api.username,
            'password':api.password
        }
    })
    system_stats = api.request('/stat/system')
    api.request('/config/logout', {'logout': {}})
    """
    
    def __init__(self, args):        
        self.host = args['--host']
        self.username = args['--username']
        self.password = args['--password']
        self.protocol = args['--protocol']
        self.base_path = args['--base_path']
        self.logging = True if args['--logging'].lower() == 'true' else False
        self.log = args['--log']
        self.log_dir = os.path.dirname(self.log)
        self.clear_log = True if args['--clear_log'].lower() == 'true' else False
        if self.log_dir and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        if self.clear_log and os.path.exists(self.log):
            open(self.log, 'w').close()
        self.session = None

    def __enter__(self):
        # login to get a session
        self.request('/config/login', {
            'login': {
                'username':self.username,
                'password':self.password
            }
        })
        return self

    def __exit__(self, type, value, traceback):
        self.request('/config/logout', {'logout': {}})

    def end_session(self):
        self.session = None

    def get_req_name(self, path):
        _path = urlparse.urlparse(path).path
        if _path.endswith('/'): _path = _path[:-1]
        return _path.rsplit('/', 1)[1]

        
    def request(self, path, payload=None, method=None):
        """
        Builds the request and returns a json object of the result or None.
        If 'payload' is specified, the request will be a POST, otherwise it will be a GET.

        :param path: a path appended to 'self.base_path' (default of '/nitro/v1'), eg: path='/config' => '/nitro/v1/config'
        :type path: str or unicode

        :param payload: the object to be passed to the server
        :type payload: dict or None

        :param method: the request method [ GET | POST | PUT | DELETE ]
        :type method: str or unicode

        :returns: the result of the request as a dictionary; 
            if result is json: return json as a dict
            if result == '': return {'headers': <headers dict>}
            if result != json and result != '': return {'result': '<text returned>'}
        :rtype: dict or None
        """
        if self.session or (self.username and self.password and payload and 'login' in payload):
            result = None
            headers = {}
            cookies = {}

            url = self.protocol+'://'+self.host+self.base_path+path
            if self.session:
                cookies['NITRO_AUTH_TOKEN'] = self.session

            if payload:
                if method and method.upper() == 'PUT':
                    response = requests.put(url, data=json.dumps(payload), headers=headers, cookies=cookies)
                else:
                    headers['Content-Type'] = 'application/vnd.com.citrix.netscaler.'+self.get_req_name(path)+'+json'
                    response = requests.post(url, data=json.dumps(payload), headers=headers, cookies=cookies)
            else:
                if method and method.upper() == 'DELETE':
                    response = requests.delete(url, headers=headers, cookies=cookies)
                else:
                    response = requests.get(url, headers=headers, cookies=cookies)

            if response.ok and payload and 'login' in payload:
                self.session = response.cookies['NITRO_AUTH_TOKEN']
                if response.text == '':
                    result = {'headers': response.headers}
                else:
                    result = {'result': response.text}
            else:
                if response.ok:
                    try:
                        result = response.json()
                    except:
                        if response.text == '':
                            result = {'headers': response.headers}
                        else:
                            result = {'result': response.text}
                else:
                    print response.text

            if payload and 'logout' in payload:
                self.end_session()
               
            if self.logging:
                with open(self.log, 'a') as f:
                    if payload:
                        f.write((method.upper() if method else "POST")+" "+url)
                        f.write('\n')
                        pprint.pprint(payload, f, 2)
                    else:
                        f.write((method.upper() if method else "GET")+" "+url)
                        f.write('\n')
                    f.write('\n')
                    if response.ok:
                        #pprint.pprint(response.headers, f, 2)  # if you want to log the headers too...
                        pprint.pprint(result, f, 2)
                    else:
                        f.write(response.text)
                        f.write('\n')
                    f.write('\n\n\n')

            return result
        else:
            print("ERROR: --host, --username and --password are required to use the api...")
            return None

if __name__ == '__main__':
    with API(args) as api:
        pprint.pprint(api.request('/stat/system'))

