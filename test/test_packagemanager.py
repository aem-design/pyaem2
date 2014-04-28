from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest

class HandlersMatcher(object):

    def __init__(self, handler_keys):
        self.handler_keys = handler_keys

    def __eq__(self, handlers):
        return handlers.keys() == self.handler_keys


class TestPackageManager(unittest.TestCase):


    def test_init(self):

        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(packagemanager.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(packagemanager.kwargs['foo'], 'bar')

        self.assertTrue(200 in packagemanager.handlers)
        self.assertTrue(401 in packagemanager.handlers)
        self.assertTrue(405 in packagemanager.handlers)


    def test_init_ok_success(self):

        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html', foo='bar')
        handler = packagemanager.handlers[200]
        response = {'body': '{ "success": true, "msg": "some message" }'}
        result = handler(response)

        self.assertEquals(result['status'], 'success')
        self.assertEquals(result['message'], 'some message')


    def test_init_ok_failure(self):

        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html', foo='bar')
        handler = packagemanager.handlers[200]
        response = {'body': '{ "success": false, "msg": "some message" }'}
        result = handler(response)

        self.assertEquals(result['status'], 'failure')
        self.assertEquals(result['message'], 'some message')


    def test_create_package(self):

        bag.request = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.create_package('mygroup', 'mypackage', '1.0-SNAPSHOT', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/etc/packages/mypackage',
            {'packageName': 'mypackage', 'cmd': 'create', 'groupName': 'mygroup', '_charset_': 'utf-8', 'packageVersion': '1.0-SNAPSHOT', 'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


if __name__ == '__main__':
    unittest.main()
    