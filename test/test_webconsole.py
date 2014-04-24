import pyaem
import unittest

class TestWebConsole(unittest.TestCase):


    def test_init(self):

        webconsole = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(webconsole.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(webconsole.kwargs['foo'], 'bar')

        self.assertTrue(401 in webconsole.handlers)
        self.assertTrue(404 in webconsole.handlers)
        self.assertTrue(405 in webconsole.handlers)


    def test_init_bundler_not_found(self):

        webconsole = pyaem.webconsole.WebConsole('http://localhost:4502/.cqactions.html', foo='bar')
        handler = webconsole.handlers[404]
        response = None
        result = handler(response, bundle_name='some_bundle_name')

        self.assertEquals(result['status'], 'failure')
        self.assertEquals(result['message'], 'Bundle some_bundle_name not found')


if __name__ == '__main__':
    unittest.main()
    