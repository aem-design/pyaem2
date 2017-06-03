PyAEM
-----

[![Build Status](https://travis-ci.org/wildone/pyaem.svg?branch=master)](https://travis-ci.org/wildone/pyaem)
[![Coverage Status](https://coveralls.io/repos/github/wildone/pyaem/badge.svg)](https://coveralls.io/github/wildone/pyaem)
[![Codeship Status for wildone/pyaem](https://app.codeship.com/projects/b6e087c0-2a8b-0135-9536-463a645743d5/status?branch=master)](https://app.codeship.com/projects/223937)

PyAEM is a Python client for [Adobe Experience Manager](http://dev.day.com/docs/en/cq/current.html) (AEM) API.

<img align="right" src="https://raw.github.com/wildone/pyaem/master/avatar.jpg" alt="Avatar"/>

Tested with AEM 5.6.1 up to 6.2 SP1 on Python 2.6 and 2.7.

Installation
------------

    pip install pyaem

Usage
-----

    import pyaem

    aem = pyaem.PyAem('admin', 'password', 'localhost', 4502)

Content Management

    aem.create_path('/content/mysite')

    aem.activate_path('/content/mysite')

    aem.does_user_exist('/home/users/m', 'myuser')

    aem.create_user('/home/users/m', 'myuser', 'mypassword')

    aem.add_user_to_group('myuser', '/home/groups/m', 'mygroup')

    aem.does_group_exist('/home/groups/m', 'mygroup')

    aem.create_group('/home/groups/m', 'mygroup')

    aem.change_password('/home/users/m', 'myuser', 'myoldpassword', 'mynewpassword')

    aem.set_permission('myuser')

    aem.create_agent('myagent', 'flush', 'someuser', 'somepassword', 'http://somehost:8080', 'publish')

    aem.delete_agent('myagent', 'publish')

    aem.set_property('/content/mysite', 'sling:target', '/welcome.html')

Package Management

    aem.create_package('mygroup', 'mypackage', 1.2.3)

    aem.update_package('mygroup', 'mypackage', 1.2.3, acHandling = 'true')

    aem.update_package_with_filter('mygroup', 'mypackage', 1.2.3, '/content/dam', acHandling = 'true')

    aem.build_package('mygroup', 'mypackage', 1.2.3)

    aem.download_package('mygroup', 'mypackage', 1.2.3, '/mnt/ephemeral0')

    aem.upload_package('mygroup', 'mypackage', 1.2.3, '/mnt/ephemeral0', force = 'true')

    aem.install_package('mygroup', 'mypackage', 1.2.3)

    aem.replicate_package('mygroup', 'mypackage', 1.2.3)

    aem.delete_package('mygroup', 'mypackage', 1.2.3)

Package Management

    aem.upload_package_sync('mygroup', 'mypackage', 1.2.3, '/mnt/ephemeral0', force = 'true')

    aem.install_package_sync('mygroup', 'mypackage', 1.2.3)

    aem.replicate_package_sync('mygroup', 'mypackage', 1.2.3)

Bundle Management

    aem.start_bundle('mybundle')

    aem.stop_bundle('mybundle')

    aem.install_bundle('mybundle', 1.2.3, '/mnt/ephemeral0')

Result And Error Handling
-------------------------

    import pyaem

    aem = pyaem.PyAem('admin', 'password', 'localhost', 4502)

    try:

        result = aem.activate_path('/content/mysite')
        result = aem.create_package('mygroup', 'pyaem-create-package', '1.2.3')
        result = aem.update_package_with_filter('mygroup', 'pyaem-create-package', '1.2.3', '/content/dam')

        # check result status
        if result.is_success():
        	print 'Success: {0}'.format(result.message)
        else:
        	print 'Failure: {0}'.format(result.message)

        # debug response and request details via result
        print result.response['http_code']
        print result.response['body']
        print result.response['request']['method']
        print result.response['request']['url']
        print result.response['request']['params']

        # debug all response and request details in a single string
        print result.debug()

    except pyaem.PyAemException, e:

        # exception message
        print e.message

        # exception code uses response http_code
        print e.code

        # debug response and request details via exception
        print e.response['http_code']
        print e.response['body']
        print e.response['request']['method']
        print e.response['request']['url']
        print e.response['request']['params']

 Development
 -----------
Dev
```bash
  apt-get install python-pip libcurl4-gnutls-dev python-dev
  make deps-dev
  make deps
  make build
```
Test
```bash
  make test
```
