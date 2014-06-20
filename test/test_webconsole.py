from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestWebConsole(unittest.TestCase):


    def setUp(self):

        self.web_console = pyaem.webconsole.WebConsole('http://localhost:4502', debug=True)
        bag.request = MagicMock()
        bag.upload_file = MagicMock()


    def test_init(self):

        self.assertEqual(self.web_console.url, 'http://localhost:4502')
        self.assertEqual(self.web_console.kwargs['debug'], True)

        self.assertTrue(401 in self.web_console.handlers)
        self.assertTrue(404 in self.web_console.handlers)
        self.assertTrue(405 in self.web_console.handlers)


    def test_init_bundle_not_found(self):

        handler = self.web_console.handlers[404]
        response = None
        result = handler(response, bundle_name='some_bundle_name')

        self.assertEquals(result.is_failure(), True)
        self.assertEquals(result.message, 'Bundle some_bundle_name not found')
        self.assertEquals(result.response, response)


    def test_start_bundle(self):

        _self = self
        class StartBundleHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response, bundle_name='mybundle')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Bundle mybundle started')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response, bundle_name='mybundle')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Bundle mybundle started')
                _self.assertEquals(result.response, response)

                return super(StartBundleHandlerMatcher, self).__eq__(handlers)

        self.web_console.start_bundle('mybundle', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/system/console/bundles/mybundle',
            {'action': 'start',
             'foo': 'bar'},
            StartBundleHandlerMatcher([200, 201, 401, 404, 405]),
            bundle_name='mybundle',
            debug=True)


    def test_stop_bundle(self):

        _self = self
        class StopBundleHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response, bundle_name='mybundle')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Bundle mybundle stopped')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response, bundle_name='mybundle')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Bundle mybundle stopped')
                _self.assertEquals(result.response, response)

                return super(StopBundleHandlerMatcher, self).__eq__(handlers)

        self.web_console.stop_bundle('mybundle', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/system/console/bundles/mybundle',
            {'action': 'stop',
             'foo': 'bar'},
            StopBundleHandlerMatcher([200, 401, 404, 405]),
            bundle_name='mybundle',
            debug=True)


    def test_install_bundle(self):

        _self = self
        class InstallBundleHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response, bundle_name='mybundle')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Bundle mybundle installed')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response, bundle_name='mybundle')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Bundle mybundle installed')
                _self.assertEquals(result.response, response)

                return super(InstallBundleHandlerMatcher, self).__eq__(handlers)

        self.web_console.install_bundle('mybundle', '1.2.3', '/mnt/ephemeral0/', foo='bar')
        bag.upload_file.assert_called_once_with(
            'http://localhost:4502/system/console/bundles',
            {'action': 'install',
             'bundlefile': (10, '/mnt/ephemeral0/mybundle-1.2.3.jar'),
             'foo': 'bar'},
            InstallBundleHandlerMatcher([200, 201, 401, 404, 405]),
            bundle_name='mybundle',
            debug=True)


if __name__ == '__main__':
    unittest.main()
