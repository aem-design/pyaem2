from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestSling(unittest.TestCase):


    def setUp(self):

        self.sling = pyaem.sling.Sling('http://localhost:4502', debug=True)
        bag.request = MagicMock()


    def test_init(self):

        self.assertEqual(self.sling.url, 'http://localhost:4502')
        self.assertEqual(self.sling.kwargs['debug'], True)

        self.assertTrue(401 in self.sling.handlers)


    def test_login(self):

        _self = self
        class LoginHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Login successfully')
                _self.assertEquals(result.response, response)

                return super(LoginHandlerMatcher, self).__eq__(handlers)

        self.sling.login(foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/sling/login',
            {'foo': 'bar'},
            LoginHandlerMatcher([200, 401]),
            debug=True)
