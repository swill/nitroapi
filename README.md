NITRO API Wrapper
=================
This project is a minimalist wrapper around the NetScaler NITRO API.  Its purpose 
is to expedite the process of testing the API and building scripts to do useful tasks.

It is expected that you refer to the NITRO documentation while using this lib.

There are two ways in which this lib can be consumed:

1. The `API` class can be instantiated from any code.  It has a single `request`
 method, which is used to make API calls against NITRO.

2. The `CLI` class is a subclass of `API` and is designed to be a convenience
 class for working with stand alone scripts that populate the `API` constructor
 using command line arguments parsed by `docopt`.  The command line arguments can be
 passed in directly or they can be added to a JSON file and the `--json` flag can
 be used to reference the JSON file path. A `cli_example.py` file is included in
 the package to give a working example of how to use this use case.

The `request` method takes a NITRO API call and returns a python dictionary with 
the result.

``` python
api.request(self, path, payload=None, method=None)
```

``` sphinx
Builds the request and returns a json object of the result or None.
If 'payload' is specified, the request will be a POST, otherwise it will be a GET.

:param path: a path appended to 'self.base_path' (default of '/nitro/v1'), 
             eg: path='/config' => '/nitro/v1/config'
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
```


**Examples using the parent `API` class:**

``` python
from nitroapi import API

# Recommended usage using WITH (to automatically login and logout):
with API(username="your user", password="your pass", endpoint="ns url") as api:
    system_stats = api.request('/stat/system')

# Manual setup and tear down example (requires explicit logout):
api = API(username="your user", password="your pass", endpoint="ns url")
api.request('/config/login', {
    'login': {
        'username':api.username,
        'password':api.password
    }
})
system_stats = api.request('/stat/system')
api.request('/config/logout', {'logout': {}})
```


**Examples using the `CLI` sub-class:**
Duplicate the `./cli_example.py` to get started.

``` python
from nitroapi import CLI

# Recommended usage using WITH (to automatically login and logout):
with CLI(__doc__) as api:
    pprint.pprint(api.request('/stat/system'))

# Manual setup and tear down example (requires explicit logout):
api = CLI(__doc__)
api.request('/config/login', {
    'login': {
        'username':api.username,
        'password':api.password
    }
})
system_stats = api.request('/stat/system')
api.request('/config/logout', {'logout': {}})
```


INSTALL
=======
The easiest way to install this library is through `pip`.

``` bash
$ pip install nitroapi
```

Alternatively, you can pull down the source code directly and install manually.

``` bash
$ git clone https://github.com/swill/nitroapi.git
$ cd nitroapi
$ python setup.py install
```


USAGE
=====
The core functionality is documented above, but it is worth spending a minute
to better describe the `CLI` use case.  

``` bash
$ ./cli_example.py --help

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
```

