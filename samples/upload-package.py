__author__ = 'maxbarrass'

import os
import time
import json
import sys
import argparse

import pyaem2

aem = pyaem2.PyAem2('admin', 'admin', 'localhost', 4502)


try:

    group_name = "day_internal/consulting"
    package_name = "com.adobe.acs.bundles.twitter4j-content"
    package_version = "1.0.0"
    file_path = "."

    result = aem.upload_package_sync(group_name, package_name, package_version, file_path, force = 'true')

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

except pyaem2.PyAem2Exception as e:

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
