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
        packagemanager.create_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/etc/packages/mypackage',
            {'packageName': 'mypackage',
             'cmd': 'create',
             'groupName': 'mygroup',
             '_charset_': 'utf-8',
             'packageVersion': '1.2.3',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


    def test_update_package(self):

        bag.request = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.update_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/.cqactions.html/crx/packmgr/update.jsp',
            {'packageName': 'mypackage',
             'groupName': 'mygroup',
             'version': '1.2.3',
             '_charset_': 'utf-8',
             'path': '/etc/packages/mygroup/mypackage-1.2.3.zip',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


    def test_build_package(self):

        bag.request = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.build_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'build',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


    def test_download_package(self):

        _self = self
        class DownloadPackageHandlerMatcher(object):

            def __init__(self, handler_keys):
                self.handler_keys = handler_keys

            def __eq__(self, handlers):

                result = handlers[200]({}, file='/tmp/somepath/mypackage-1.2.3.zip')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], '/tmp/somepath/mypackage-1.2.3.zip was successfully downloaded')

                return handlers.keys() == self.handler_keys

        bag.download_file = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.download_package('mygroup', 'mypackage', '1.2.3', '/tmp/somepath', foo='bar')
        bag.download_file.assert_called_once_with(
            'http://localhost:4502/.cqactions.html/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'foo': 'bar'},
            DownloadPackageHandlerMatcher([200, 401, 405]),
            file='/tmp/somepath/mypackage-1.2.3.zip')


    def test_upload_package(self):

        _self = self
        class UploadPackageHandlerMatcher(object):

            def __init__(self, handler_keys):
                self.handler_keys = handler_keys

            def __eq__(self, handlers):

                result = handlers[200](
                    {'body': '{"success": true, "msg": "some message"}'},
                    file='/tmp/somepath/mypackage-1.2.3.zip')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'some message')

                return handlers.keys() == self.handler_keys

        bag.upload_file = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.upload_package('mygroup', 'mypackage', '1.2.3', '/tmp/somepath', foo='bar')
        bag.upload_file.assert_called_once_with(
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/',
            {'cmd': 'upload',
             'foo': 'bar',
             'package': (10, '/tmp/somepath/mypackage-1.2.3.zip')},
            UploadPackageHandlerMatcher([200, 401, 405]),
            file_name='mypackage-1.2.3.zip')


    def test_install_package(self):

        bag.request = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.install_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'install',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


    def test_replicate_package(self):

        bag.request = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.replicate_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'replicate',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


    def test_delete_package(self):

        bag.request = MagicMock()
        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html')
        packagemanager.delete_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'delete',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


if __name__ == '__main__':
    unittest.main()
    