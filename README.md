<img align="right" src="https://raw.github.com/cliffano/pyaem/master/avatar.jpg" alt="Avatar"/>

[![Build Status](https://secure.travis-ci.org/cliffano/pyaem.png?branch=master)](http://travis-ci.org/cliffano/pyaem)
[![Coverage Status](https://coveralls.io/repos/cliffano/pyaem/badge.png?branch=master)](https://coveralls.io/r/cliffano/pyaem?branch=master)
[![Published Version](https://badge.fury.io/py/pyaem.svg)](http://badge.fury.io/py/coveralls)
<br/>

PyAEM
-----

PyAEM is a Python client for [Adobe Experience Manager](http://dev.day.com/docs/en/cq/current.html) (AEM) API.

Tested with AEM 5.6.1

Installation
------------

NOTE: This package is still a work in progress, not yet published to PyPI.

To use master:

* Add https://github.com/cliffano/pyaem/archive/master.zip to your requirements.txt file
* Run pip install --requirement requirements.txt 

And later on when pyaem is published to PyPI:

    pip install pyaem

Usage
-----

    import pyaem

    aem = pyaem.PyAem('admin', 'password', 'localhost', 4502)

Content Management

    aem.create_path('/content/mysite')

    aem.activate_path('/content/mysite')

    aem.create_user('/home/users/m', 'myuser', 'mypassword')

    aem.add_user_to_group('myuser', '/home/groups/m', 'mygroup')

    aem.create_group('/home/groups/m', 'mygroup')

    aem.change_password('/home/users/m', 'myuser', 'myoldpassword', 'mynewpassword')

    aem.set_permission('myuser')

    aem.set_agent('myagent', 'runmode')

Package Management

    aem.create_package('mygroup', 'mypackage', 1.2.3)

    aem.update_package('mygroup', 'mypackage', 1.2.3, acHandling = 'true')

    aem.build_package('mygroup', 'mypackage', 1.2.3)

    aem.download_package('mygroup', 'mypackage', 1.2.3, '/mnt/ephemeral0')

    aem.upload_package('mygroup', 'mypackage', 1.2.3, '/mnt/ephemeral0', force = 'true')

    aem.install_package('mygroup', 'mypackage', 1.2.3)

    aem.replicate_package('mygroup', 'mypackage', 1.2.3)

    aem.delete_package('mygroup', 'mypackage', 1.2.3)
    
Bundle Management

    aem.start_bundle('mybundle')

    aem.stop_bundle('mybundle')

    aem.install_bundle('mybundle')

Error Handling
--------------

    try:
    
        result = aem.activate_path('/content/mysite')
        
        if result['status'] == 'success':
        	print 'It works: {0}'.format(result['message'])
        else:
        	print 'An error occurred: {0}'.format(result['message'])
        	
    except pyaem.PyAemException, e:
    
        print e.message
        
TODO
----

* Improve test coverage
* Improve code documentation
* Generate project site
