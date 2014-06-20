from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestPackageManagerServiceJsp(unittest.TestCase):


    def setUp(self):

        self.package_manager = pyaem.packagemanagerservicejsp.PackageManagerServiceJsp(
            'http://localhost:4502', debug=True)
        bag.request = MagicMock()
        bag.download_file = MagicMock()
        bag.upload_file = MagicMock()


    def test_init(self):

        self.assertEqual(self.package_manager.url, 'http://localhost:4502')
        self.assertEqual(self.package_manager.kwargs['debug'], True)

        self.assertTrue(401 in self.package_manager.handlers)


    def test_is_package_uploaded(self):

        _self = self
        class IsPackageUploadedHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                # non-ok status
                response = {'body': '<crx><response><status code="500">notok</status></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message,
                    'Unable to retrieve package list. Command status code 500 and status value notok')
                _self.assertEquals(result.response, response)

                # two packages with one matching
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>yourgroup</group><name>yourpackage</name><version>4.5.6</version></package>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is uploaded')
                _self.assertEquals(result.response, response)

                # one non-matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>yourgroup</group><name>yourpackage</name><version>4.5.6</version></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is not uploaded')
                _self.assertEquals(result.response, response)

                # one matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is uploaded')
                _self.assertEquals(result.response, response)

                # no package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is not uploaded')
                _self.assertEquals(result.response, response)

                return super(IsPackageUploadedHandlerMatcher, self).__eq__(handlers)

        self.package_manager.is_package_uploaded('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/crx/packmgr/service.jsp',
            {'cmd': 'ls',
             'foo': 'bar'},
            IsPackageUploadedHandlerMatcher([200, 401]),
            debug=True)


    def test_is_package_uploaded_nover(self):

        _self = self
        class IsPackageUploadedHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                # one matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>mygroup</group><name>mypackage</name><version></version></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage- is uploaded')
                _self.assertEquals(result.response, response)

                # one non matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage- is not uploaded')
                _self.assertEquals(result.response, response)

                return super(IsPackageUploadedHandlerMatcher, self).__eq__(handlers)

        self.package_manager.is_package_uploaded('mygroup', 'mypackage', '', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/crx/packmgr/service.jsp',
            {'cmd': 'ls',
             'foo': 'bar'},
            IsPackageUploadedHandlerMatcher([200, 401]),
            debug=True)


    def test_is_package_installed(self):

        _self = self
        class IsPackageInstalledHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                # non-ok status
                response = {'body': '<crx><response><status code="500">notok</status></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message,
                    'Unable to retrieve package list. Command status code 500 and status value notok')
                _self.assertEquals(result.response, response)

                # one matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version>' +
                    '<lastUnpackedBy>admin</lastUnpackedBy></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is installed')
                _self.assertEquals(result.response, response)

                # two packages with one matching
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>yourgroup</group><name>yourpackage</name><version>4.5.6</version>' +
                    '<lastUnpackedBy>admin</lastUnpackedBy></package>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version>' +
                    '<lastUnpackedBy>admin</lastUnpackedBy></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is installed')
                _self.assertEquals(result.response, response)

                # two packages with none matching
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>yourgroup</group><name>yourpackage</name><version>4.5.6</version>' +
                    '<lastUnpackedBy>null</lastUnpackedBy></package>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version>' +
                    '<lastUnpackedBy>null</lastUnpackedBy></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is not installed')
                _self.assertEquals(result.response, response)

                # no package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage-1.2.3 is not installed')
                _self.assertEquals(result.response, response)

                return super(IsPackageInstalledHandlerMatcher, self).__eq__(handlers)

        self.package_manager.is_package_installed('mygroup', 'mypackage', '1.2.3', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/crx/packmgr/service.jsp',
            {'cmd': 'ls',
             'foo': 'bar'},
            IsPackageInstalledHandlerMatcher([200, 401]),
            debug=True)


    def test_is_package_installed_nover(self):

        _self = self
        class IsPackageInstalledHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                # one matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>mygroup</group><name>mypackage</name><version></version>' +
                    '<lastUnpackedBy>admin</lastUnpackedBy></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage- is installed')
                _self.assertEquals(result.response, response)

                # no matching package
                response = {'body': '<crx><response><status code="200">ok</status><data><packages>' +
                    '<package><group>mygroup</group><name>mypackage</name><version>1.2.3</version>' +
                    '<lastUnpackedBy>admin</lastUnpackedBy></package>' +
                    '</packages></data></response></crx>'}
                result = handlers[200](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Package mygroup/mypackage- is not installed')
                _self.assertEquals(result.response, response)

                return super(IsPackageInstalledHandlerMatcher, self).__eq__(handlers)

        self.package_manager.is_package_installed('mygroup', 'mypackage', '', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/crx/packmgr/service.jsp',
            {'cmd': 'ls',
             'foo': 'bar'},
            IsPackageInstalledHandlerMatcher([200, 401]),
            debug=True)


if __name__ == '__main__':
    unittest.main()

