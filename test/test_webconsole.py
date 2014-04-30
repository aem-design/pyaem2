from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestWebConsole(unittest.TestCase):


    def test_init(self):

        web_console = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(web_console.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(web_console.kwargs['foo'], 'bar')

        self.assertTrue(401 in web_console.handlers)
        self.assertTrue(404 in web_console.handlers)
        self.assertTrue(405 in web_console.handlers)


    def test_init_bundler_not_found(self):

        web_console = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html', foo='bar')
        handler = web_console.handlers[404]
        response = None
        result = handler(response, bundle_name='some_bundle_name')

        self.assertEquals(result['status'], 'failure')
        self.assertEquals(result['message'], 'Bundle some_bundle_name not found')


    def test_start_bundle(self):

        _self = self
        class StartBundleHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):
                result = handlers[200]({}, bundle_name='mybundle')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Bundle mybundle was successfully started')
                return handlers.keys() == self.handler_keys

        bag.request = MagicMock()
        web_console = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html')
        web_console.start_bundle('mybundle', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/system/console/bundles/mybundle',
            {'action': 'start',
             'foo': 'bar'},
            StartBundleHandlerMatcher([200, 401, 404, 405]),
            bundle_name='mybundle')


    def test_stop_bundle(self):

        _self = self
        class StopBundleHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):
                result = handlers[200]({}, bundle_name='mybundle')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Bundle mybundle was successfully stopped')
                return handlers.keys() == self.handler_keys

        bag.request = MagicMock()
        web_console = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html')
        web_console.stop_bundle('mybundle', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/system/console/bundles/mybundle',
            {'action': 'stop',
             'foo': 'bar'},
            StopBundleHandlerMatcher([200, 401, 404, 405]),
            bundle_name='mybundle')


    def test_install_bundle(self):

        _self = self
        class InstallBundleHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):
                result = handlers[200]({}, bundle_name='mybundle')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Bundle mybundle was successfully installed')
                return handlers.keys() == self.handler_keys

        bag.upload_file = MagicMock()
        web_console = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html')
        web_console.install_bundle('mybundle', '1.2.3', foo='bar')
        bag.upload_file.assert_called_once_with(
            'http://localhost:4502/.cqactions.html/system/console/bundles',
            {'action': 'install',
             'bundlefile': (10, 'mybundle-1.2.3.zip'),
             'foo': 'bar'},
            InstallBundleHandlerMatcher([200, 401, 404, 405]),
            bundle_name='mybundle')


if __name__ == '__main__':
    unittest.main()
    