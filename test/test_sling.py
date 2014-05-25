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


    def test_is_valid_login(self):

        _self = self
        class IsValidLoginHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Login is valid')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[401](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Login is invalid')
                _self.assertEquals(result.response, response)

                return super(IsValidLoginHandlerMatcher, self).__eq__(handlers)

        self.sling.is_valid_login(foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/system/sling/login',
            {'foo': 'bar'},
            IsValidLoginHandlerMatcher([200, 401]),
            debug=True)
