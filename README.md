NITRO API Wrapper
=================
This project is a minimalist wrapper around the NetScaler NITRO API.  Its purpose 
is to expedite the process of testing the API and building scripts to do useful tasks.

This project exposes a single `API` class with a simple `request` method.  This 
method takes a NITRO API call and returns a python dictionary with the result.

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

Here is a simple example using the `with` statment:

``` python
with API(args) as api:
    system_stats = api.request('/stat/system')
```

It is also possible to manually create and remove the session:

``` python
api = API(args)
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
This project does not need to be installed, it can be run in-place.  
However, it does depend on a few libraries to keep things simple.

docops
------

``` bash
$ pip install docops
```

requests
--------

``` bash
$ pip install requests
```


USAGE
=====
The usage for this project is documented in the 'help' section of the scripts.

``` bash
$ ./nitro_api.py --help
```

```
Usage:
  nitro_api.py (--host=<arg> --username=<arg> --password=<arg>) [options]
  nitro_api.py (-h | --help)

Options:
  -h --help             Show this screen.
  --host=<arg>          NetScaler IP.
  --username=<arg>      NetScaler username.
  --password=<arg>      NetScaler password.
  --protocol=<arg>      Protocol used to connect to the NetScaler (http | https) 
                        [default: http].
  --base_path=<arg>     Base NetScaler API path [default: /nitro/v1].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log=<arg>           The log file to be used [default: logs/nitro_api.log].
  --clear_log=<arg>     Removes the log each time the API object is created 
                        [default: True].
```

``` bash
$ ./api_examples.py --help
```

```
Usage:
  api_examples.py (--host=<arg> --username=<arg> --password=<arg>) [options]
  api_examples.py (-h | --help)

Options:
  -h --help             Show this screen.
  --host=<arg>          NetScaler IP.
  --username=<arg>      NetScaler username.
  --password=<arg>      NetScaler password.
  --protocol=<arg>      Protocol used to connect to the NetScaler (http | https) 
                        [default: http].
  --base_path=<arg>     Base NetScaler API path [default: /nitro/v1].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log=<arg>           The log file to be used [default: logs/nitro_api.log].
  --clear_log=<arg>     Removes the log each time the API object is created 
                        [default: True].
```

This project can be run as a stand alone script or the `API` object can be imported into other scripts in this directory as a library.

`nitro_api.py` is a stand alone script which can be run on its own, as well as a basic library which can be imported into other scripts.

`api_examples.py` is an example of using the `nitro_api.py` script as a library.  In this example, we  simply import the `API` object and start making requests.  This is ideal if you have multiple scripts that do different tasks and you want them to all exist at the same time.  Simply duplicate this file and change the api requests as needed.

