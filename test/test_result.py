import pyaem
import unittest

class TestResult(unittest.TestCase):


    def setUp(self):

        response = {'body': 'some body'}
        self.result = pyaem.PyAemResult(response)

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

        result = pyaem.PyAemResult(response)
        result.success('some message')

        self.assertEqual(result.debug(),
            'Response body: <html>some html here</html>\n' +
            'Request parameters: {\'foo\': \'bar\'}\n' +
            'Result status: success\n' +
            'Result message: some message\n' +
            'Request URL: http://localhost:4502\n' +
            'Request method: get\n' +
            'Response code: 200\n')


if __name__ == '__main__':
    unittest.main()
    