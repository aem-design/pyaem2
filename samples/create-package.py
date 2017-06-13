__author__ = 'maxbarrass'

import pyaem

aem = pyaem.PyAem('admin', 'admin', 'localhost', 4502)

try:

    result = aem.create_package('mygroup', 'pyaem-create-package', '1.2.3')
    result = aem.update_package_with_filter('mygroup', 'pyaem-create-package', '1.2.3', '/content/dam')

    # check result status
    if result.is_success():
        print('Success: {0}'.format(result.message))
    else:
        print('Failure: {0}'.format(result.message))

    # debug response and request details via result
    print(result.response['http_code'])
    print(result.response['body'])
    print(result.response['request']['method'])
    print(result.response['request']['url'])
    print(result.response['request']['params'])

    # debug all response and request details in a single string
    print(result.debug())

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
