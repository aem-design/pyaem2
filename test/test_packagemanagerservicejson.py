from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestPackageManagerServiceJson(unittest.TestCase):


    def setUp(self):

        self.package_manager = pyaem.packagemanagerservicejson.PackageManagerServiceJson(
            'http://localhost:4502', debug=True)
        bag.request = MagicMock()
        bag.download_file = MagicMock()
        bag.upload_file = MagicMock()


    def test_init(self):

        self.assertEqual(self.package_manager.url, 'http://localhost:4502')
        self.assertEqual(self.package_manager.kwargs['debug'], True)

        self.assertTrue(200 in self.package_manager.handlers)
        self.assertTrue(401 in self.package_manager.handlers)
        self.assertTrue(405 in self.package_manager.handlers)


    def test_init_ok_success(self):

        handler = self.package_manager.handlers[200]
        response = {'body': '{ "success": true, "msg": "some message" }'}
        result = handler(response)

        self.assertEquals(result.is_success(), True)
        self.assertEquals(result.message, 'some message')
        self.assertEquals(result.response, response)


    def test_init_ok_failure(self):

        handler = self.package_manager.handlers[200]
        response = {'body': '{ "success": false, "msg": "some message" }'}
        result = handler(response)

        self.assertEquals(result.is_failure(), True)
        self.assertEquals(result.message, 'some message')
        self.assertEquals(result.response, response)


    def test_create_package(self):

        self.package_manager.create_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/.json/etc/packages/mypackage',
            {'packageName': 'mypackage',
             'cmd': 'create',
             'groupName': 'mygroup',
             '_charset_': 'utf-8',
             'packageVersion': '1.2.3',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]),
            debug=True)


    def test_build_package(self):

        self.package_manager.build_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'build',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]),
            debug=True)


    def test_upload_package(self):

        _self = self
        class UploadPackageHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = {'body': '{"success": true, "msg": "some message"}'}
                result = handlers[200](response, file='/tmp/somepath/mypackage-1.2.3.zip')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'some message')
                _self.assertEquals(result.response, response)

                response = {'body': '{"success": false, "msg": "some message"}'}
                result = handlers[200](response, file='/tmp/somepath/mypackage-1.2.3.zip')
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'some message')
                _self.assertEquals(result.response, response)

                return super(UploadPackageHandlerMatcher, self).__eq__(handlers)

        self.package_manager.upload_package('mygroup', 'mypackage', '1.2.3', '/tmp/somepath/', foo='bar')
        bag.upload_file.assert_called_once_with(
            'http://localhost:4502/crx/packmgr/service/.json/',
            {'cmd': 'upload',
             'foo': 'bar',
             'package': (10, '/tmp/somepath/mypackage-1.2.3.zip')},
            UploadPackageHandlerMatcher([200, 401, 405]),
            file_name='mypackage-1.2.3.zip',
            debug=True)


    def test_install_package(self):

        _self = self
        class InstallPackageHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = {'body': '{"success": true, "msg": "some message"}'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'some message')
                _self.assertEquals(result.response, response)

                response = {'body': '{"success": false, "msg": "some message"}'}
                result = handlers[201](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message,
                    'AEM message: some message - ' +
                    'Installation failure, package status is uploaded but not installed')
                _self.assertEquals(result.response, response)

                return super(InstallPackageHandlerMatcher, self).__eq__(handlers)

        self.package_manager.install_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'install',
             'foo': 'bar'},
            InstallPackageHandlerMatcher([200, 201, 401, 405]),
            debug=True)


    def test_install_package_spaces(self):

        self.package_manager.install_package('mygroup', 'CQ 5.6.1 Security Service Pack', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/.json/' +
                'etc/packages/mygroup/CQ%205.6.1%20Security%20Service%20Pack-1.2.3.zip',
            {'cmd': 'install',
             'foo': 'bar'},
            HandlersMatcher([200, 201, 401]),
            debug=True)


    def test_replicate_package(self):

        self.package_manager.replicate_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'replicate',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]),
            debug=True)


    def test_delete_package(self):

        self.package_manager.delete_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/.json/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'delete',
             'foo': 'bar'},
            HandlersMatcher([200, 401, 405]),
            debug=True)


if __name__ == '__main__':
    unittest.main()
    