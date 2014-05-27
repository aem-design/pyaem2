from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestPackageManager(unittest.TestCase):


    def setUp(self):

        self.package_manager = pyaem.packagemanager.PackageManager('http://localhost:4502', debug=True)
        bag.request = MagicMock()
        bag.download_file = MagicMock()
        bag.upload_file = MagicMock()


    def test_init(self):

        self.assertEqual(self.package_manager.url, 'http://localhost:4502')
        self.assertEqual(self.package_manager.kwargs['debug'], True)

        self.assertTrue(401 in self.package_manager.handlers)
        self.assertTrue(405 in self.package_manager.handlers)


    def test_update_package(self):

        _self = self
        class UpdatePackageHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                result = handlers[200](None)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package updated')
                _self.assertEquals(result.response, None)

                return super(UpdatePackageHandlerMatcher, self).__eq__(handlers)

        self.package_manager.update_package('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/crx/packmgr/update.jsp',
            {'packageName': 'mypackage',
             'groupName': 'mygroup',
             'version': '1.2.3',
             '_charset_': 'utf-8',
             'path': '/etc/packages/mygroup/mypackage-1.2.3.zip',
             'foo': 'bar'},
            UpdatePackageHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_download_package(self):

        _self = self
        class DownloadPackageHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                result = handlers[200](None, file='/tmp/somepath/mypackage-1.2.3.zip')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, '/tmp/somepath/mypackage-1.2.3.zip downloaded')
                _self.assertEquals(result.response, None)

                return super(DownloadPackageHandlerMatcher, self).__eq__(handlers)

        self.package_manager.download_package('mygroup', 'mypackage', '1.2.3', '/tmp/somepath', foo='bar')
        bag.download_file.assert_called_once_with(
            'http://localhost:4502/etc/packages/mygroup/mypackage-1.2.3.zip',
            {'foo': 'bar'},
            DownloadPackageHandlerMatcher([200, 401, 405]),
            file='/tmp/somepath/mypackage-1.2.3.zip',
            debug=True)


if __name__ == '__main__':
    unittest.main()
    