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

from docopt import docopt
import json
import os
import pprint
import requests
import urlparse
import urllib
import logging as _logging

class API(object):
    """
    Login and run queries against the Nitro API for NetScaler 10.x+.

    ## Recommended usage using WITH (to automatically login and logout):
    with API(username="your user", password="your pass", endpoint="ns url") as api:
        system_stats = api.request('/stat/system')

    ## Manual setup and tear down example (requires explicit logout):
    api = API(username="your user", password="your pass", endpoint="ns url")
    api.request('/config/login', {
        'login': {
            'username':api.username,
            'password':api.password
        }
    })
    system_stats = api.request('/stat/system')
    api.request('/config/logout', {'logout': {}})
    """
    
    def __init__(
            self, 
            username,
            password,
            endpoint,
            base_path="/nitro/v1",
            logging=True,
            log_level="DEBUG",
            log="",
            clear_log=True,
            verify_ssl=True):

        self.username = username
        self.password = password
        self.endpoint = endpoint
        self.base_path = base_path
        self.logging = logging
        self.log = log
        self.log_dir = os.path.dirname(self.log)
        self.clear_log = clear_log
        self.verify_ssl = verify_ssl
        self.session = None

        self.log_level = 0
        log_levels = {
            "CRITICAL": 50,
            "ERROR": 40,
            "WARNING": 30,
            "INFO": 20,
            "DEBUG": 10,
            "NOTSET": 0
        }
        if log_level.upper() in log_levels:
            self.log_level = log_levels[log_level.upper()]

        if self.logging:
            if self.log_dir and not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            if self.clear_log and os.path.exists(self.log):
                open(self.log, 'w').close()

            _logging.basicConfig(
                filename=self.log,
                level=self.log_level,
                format='%(asctime)s %(message)s',
                datefmt='%d-%m-%Y %I:%M:%S %p' 
            )

            self.logger = _logging.getLogger(__name__)


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
            headers = {'Accept':'application/json', 'Connection':'keep-alive'}
            cookies = {}

            url = '%s/%s/%s' % (self.endpoint.rstrip('/'), self.base_path.strip('/'), path.strip('/'))
            if self.session:
                cookies['NITRO_AUTH_TOKEN'] = self.session

            if payload:
                if method and method.upper() == 'PUT':
                    response = requests.put(url, data=json.dumps(payload), headers=headers, cookies=cookies, verify=self.verify_ssl)
                else:
                    headers['Content-Type'] = 'application/vnd.com.citrix.netscaler.'+self.get_req_name(path)+'+json'
                    response = requests.post(url, data=json.dumps(payload), headers=headers, cookies=cookies, verify=self.verify_ssl)
            else:
                if method and method.upper() == 'DELETE':
                    response = requests.delete(url, headers=headers, cookies=cookies, verify=self.verify_ssl)
                else:
                    response = requests.get(url, headers=headers, cookies=cookies, verify=self.verify_ssl)

            if response.ok and payload and 'login' in payload:
                self.session = response.cookies['NITRO_AUTH_TOKEN']
                if response.text == '':
                    result = {'headers': dict(response.headers)}
                else:
                    result = {'result': response.text}
            else:
                if response.ok:
                    try:
                        result = dict(response.json())
                    except:
                        if response.text == '':
                            result = {'headers': dict(response.headers)}
                        else:
                            result = {'result': response.text}
                elif self.logging:
                    self.logger.error(response.text)

            if payload and 'logout' in payload:
                self.end_session()
               
            if self.logging:
                if payload:
                    self.logger.info("%s %s" % (method.upper() if method else "POST", url))
                    self.logger.debug("Request Headers: \n%s\n" % pprint.pformat(headers, indent=2))
                    if 'login' in payload:
                        masked = payload
                        masked['login']['password'] = '...masked...'
                        self.logger.debug("Request Payload: \n%s\n" % pprint.pformat(masked, indent=2))
                    else:
                        self.logger.debug("Request Payload: \n%s\n" % pprint.pformat(payload, indent=2))
                else:
                    self.logger.info("%s %s" % (method.upper() if method else "GET", url))
                    self.logger.debug("Request Headers: \n%s\n" % pprint.pformat(headers, indent=2))
                if response.ok:
                    self.logger.debug("Response Headers: \n%s\n" % pprint.pformat(dict(response.headers), indent=2))
                    self.logger.info("Response Object: \n%s\n" % pprint.pformat(result, indent=2))
                else:
                    self.logger.info("Response Text: \n%s\n" % response.text)

            return result
        else:
            print("ERROR: endpoint, username and password are required to use the api...")
            return None
