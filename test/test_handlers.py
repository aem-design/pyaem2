import pyaem
import unittest

class TestHandlers(unittest.TestCase):


    def test_auth_fail(self):

        response = {
            'http_code': 401,
            'body': 'some body'
        }

        try:
            pyaem.handlers.auth_fail(response)
            self.fail('An exception should have been raised')
        except pyaem.PyAemException as exception:
            self.assertEqual(exception.code, 401)
            self.assertEqual(exception.message, 'Authentication failed - incorrect username and/or password')
            self.assertEqual(exception.response, response)


    def test_method_not_allowed(self):

        response = {
            'http_code': 405,
            'body': '<html><body><title>some error message</title></body></html>'
        }

        try:
            pyaem.handlers.method_not_allowed(response)
            self.fail('An exception should have been raised')
        except pyaem.PyAemException as exception:
            self.assertEqual(exception.code, 405)
            self.assertEqual(exception.message, 'some error message')
            self.assertEqual(exception.response, response)

    def test_unexpected(self):

        response = {
            'http_code': 500,
            'body': 'some unexpected server error'
        }

        try:
            pyaem.handlers.unexpected(response)
            self.fail('An exception should have been raised')
        except pyaem.PyAemException as exception:
            self.assertEqual(exception.code, 500)
            self.assertEqual(
                exception.message, 'Unexpected response\nhttp code: 500\nbody:\nsome unexpected server error')
            self.assertEqual(exception.response, response)

if __name__ == '__main__':
    unittest.main()
    