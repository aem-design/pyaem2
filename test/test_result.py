import unittest
import pyaem2


class TestResult(unittest.TestCase):
    def setUp(self):
        response = {'body': 'some body'}
        self.result = pyaem2.PyAem2Result(response)

    def test_init(self):
        self.assertEqual(self.result.response['body'], 'some body')
        self.assertEqual(self.result.status, None)
        self.assertEqual(self.result.message, None)

    def test_success(self):
        self.result.success('some message')
        self.assertEqual(self.result.response['body'], 'some body')
        self.assertEqual(self.result.is_success(), True)
        self.assertEqual(self.result.message, 'some message')

    def test_failure(self):
        self.result.failure('some message')
        self.assertEqual(self.result.response['body'], 'some body')
        self.assertEqual(self.result.is_failure(), True)
        self.assertEqual(self.result.message, 'some message')

    def test_is_success(self):
        self.assertEqual(self.result.is_success(), False)
        self.assertEqual(self.result.is_failure(), False)
        self.result.success('some message')
        self.assertEqual(self.result.is_success(), True)
        self.assertEqual(self.result.is_failure(), False)

    def test_is_failure(self):
        self.assertEqual(self.result.is_success(), False)
        self.assertEqual(self.result.is_failure(), False)
        self.result.failure('some message')
        self.assertEqual(self.result.is_success(), False)
        self.assertEqual(self.result.is_failure(), True)

    def test_debug(self):
        response = {
            'request': {
                'method': 'get',
                'url': 'http://localhost:4502',
                'params': {'foo': 'bar'}
            },
            'http_code': 200,
            'body': '<html>some html here</html>'
        }

        response_data = {
            'Request method': response['request']['method'],
            'Request URL': response['request']['url'],
            'Request parameters': response['request']['params'],
            'Response code': response['http_code'],
            'Response body': response['body'],
            'Result status': 'success',
            'Result message': 'some message'
        }

        response_debug = ''
        for key in response_data:
            response_debug += '{0}: {1}\n'.format(key, response_data[key])

        result = pyaem2.PyAem2Result(response)
        result.success('some message')

        self.assertEqual(result.debug(), response_debug)



if __name__ == '__main__':
    unittest.main()
