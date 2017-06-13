__author__ = 'maxbarrass'

import os
import time
import json
import sys
import argparse

import pyaem

aem = pyaem.PyAem('admin', 'admin', 'localhost', 4502)


try:

    path_name = "test"
    path_base = "/content/pytest/*"
    path_type = "nt:OrderedFolder"

    params = { ':nameHint': path_name, 'jcr:primaryType': path_type, 'jcr:mixinTypes': 'rep:AccessControllable' }

    try:
        result = aem.create_path(path_base, **params)

        if result.is_failure():
            print(json.dumps({ 'failed': True, 'msg': result.message }))
        else:
            print(json.dumps({ 'msg': result.message }))
    except pyaem.PyAemException as e:
        print(json.dumps({ 'msg': 'Allow error due to inability to differentiate existing path from real error when response code is 500' + e.response['body'] }))

except pyaem.PyAemException as e:

    # exception message
    print(e.message)

    # exception code uses response http_code
    print(e.code)

    # debug response and request details via exception
    print(e.response['http_code'])
    print(e.response['body'])
    print(e.response['request']['method'])
    print(e.response['request']['url'])
    print(e.response['request']['params'])
