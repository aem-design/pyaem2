import pyaem
import unittest

class TestHandlers(unittest.TestCase):


    def test_auth_fail(self):

        response = {
            'http_code': 401
        }

        try:
            pyaem.handlers.auth_fail(response)
            self.fail('An exception should have been raised')
        except pyaem.PyAemException as e:
            self.assertEqual(e.code, 401)
            self.assertEqual(e.message, 'Authentication failed - incorrect username and/or password')


    def test_method_not_allowed(self):

        response = {
            'http_code': 405,
            'body'     : '<html><body><p>some error message</p></body></html>'
        }

        try:
            pyaem.handlers.method_not_allowed(response)
            self.fail('An exception should have been raised')
        except pyaem.PyAemException as e:
            self.assertEqual(e.code, 405)
            self.assertEqual(e.message, 'some error message')


    def test_unexpected(self):

        response = {
            'http_code': 500,
            'body'     : 'some unexpected server error'
        }

        try:
            pyaem.handlers.unexpected(response)
            self.fail('An exception should have been raised')
        except pyaem.PyAemException as e:
            self.assertEqual(e.code, 500)
            self.assertEqual(e.message, 'Unexpected response\nhttp code: 500\nbody:\nsome unexpected server error')


if __name__ == '__main__':
    unittest.main()
    