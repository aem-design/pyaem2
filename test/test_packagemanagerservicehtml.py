from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestPackageManagerServiceHtml(unittest.TestCase):


    def setUp(self):

        self.package_manager_sync = pyaem.packagemanagerservicehtml.PackageManagerServiceHtml(
            'http://localhost:4502', debug=True)
        bag.request = MagicMock()
        bag.download_file = MagicMock()
        bag.upload_file = MagicMock()


    def test_init(self):

        self.assertEqual(self.package_manager_sync.url, 'http://localhost:4502')
        self.assertEqual(self.package_manager_sync.kwargs['debug'], True)

        self.assertTrue(200 in self.package_manager_sync.handlers)
        self.assertTrue(201 in self.package_manager_sync.handlers)
        self.assertTrue(401 in self.package_manager_sync.handlers)


    def test_init_ok(self):

        handler = self.package_manager_sync.handlers[200]
        response = {'body': '<textarea>{ "success": true, "msg": "some message" }</textarea>'}
        result = handler(response)

        self.assertEquals(result.is_success(), True)
        self.assertEquals(result.message, 'some message')
        self.assertEquals(result.response, response)


    def test_init_ok_failure(self):

        handler = self.package_manager_sync.handlers[200]
        response = {'body': '<textarea>{ "success": false, "msg": "some message" }</textarea>'}
        result = handler(response)

        self.assertEquals(result.is_failure(), True)
        self.assertEquals(result.message, 'some message')
        self.assertEquals(result.response, response)


    def test_init_created(self):

        handler = self.package_manager_sync.handlers[201]
        response = {'body': '<td><div id="Message">some message</div></td>'}
        result = handler(response)

        self.assertEquals(result.is_success(), True)
        self.assertEquals(result.message, 'some message')
        self.assertEquals(result.response, response)


    def test_upload_package(self):

        self.package_manager_sync.upload_package('mygroup', 'mypackage', '1.2.3', '/tmp/somepath', foo='bar')
        bag.upload_file.assert_called_once_with(
            'http://localhost:4502/crx/packmgr/service/script.html/',
            {'cmd': 'upload',
             'foo': 'bar',
             'package': (10, '/tmp/somepath/mypackage-1.2.3.zip')},
            HandlersMatcher([200, 201, 401]),
            file_name='mypackage-1.2.3.zip',
            debug=True)


    def test_install_package(self):

        _self = self
        class InstallPackageHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = {'body': '<textarea>{ "success": true, "msg": "some message" }</textarea>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'some message')
                _self.assertEquals(result.response, response)

                response = {'body': '<textarea>{ "success": true, "msg": "some message" }</textarea>'}
                result = handlers[201](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message,
                    'Installation failure, package status is uploaded but not installed')
                _self.assertEquals(result.response, response)

                return super(InstallPackageHandlerMatcher, self).__eq__(handlers)

        self.package_manager_sync.install_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/script.html/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'install',
             'foo': 'bar'},
            InstallPackageHandlerMatcher([200, 201, 401]),
            debug=True)


    def test_install_package_spaces(self):

        self.package_manager_sync.install_package('mygroup', 'CQ 5.6.1 Security Service Pack', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/script.html/' +
                'etc/packages/mygroup/CQ%205.6.1%20Security%20Service%20Pack-1.2.3.zip',
            {'cmd': 'install',
             'foo': 'bar'},
            HandlersMatcher([200, 201, 401]),
            debug=True)


    def test_replicate_package(self):

        self.package_manager_sync.replicate_package(
            'mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/crx/packmgr/service/script.html/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'cmd': 'replicate',
             'foo': 'bar'},
            HandlersMatcher([200, 201, 401]),
            debug=True)


if __name__ == '__main__':
    unittest.main()
    