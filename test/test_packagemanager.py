import pyaem
import unittest

class TestPackageManager(unittest.TestCase):


    def test_init(self):

        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(packagemanager.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(packagemanager.kwargs['foo'], 'bar')

        self.assertTrue(200 in packagemanager.handlers)
        self.assertTrue(401 in packagemanager.handlers)
        self.assertTrue(405 in packagemanager.handlers)


    def test_init_ok_success(self):

        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html', foo='bar')
        handler = packagemanager.handlers[200]
        response = {'body': '{ "success": true, "msg": "some message" }'}
        result = handler(response)

        self.assertEquals(result['status'], 'success')
        self.assertEquals(result['message'], 'some message')


    def test_init_ok_failure(self):

        packagemanager = pyaem.packagemanager.PackageManager('http://localhost:4502/.cqactions.html', foo='bar')
        handler = packagemanager.handlers[200]
        response = {'body': '{ "success": false, "msg": "some message" }'}
        result = handler(response)

        self.assertEquals(result['status'], 'failure')
        self.assertEquals(result['message'], 'some message')


if __name__ == '__main__':
    unittest.main()
    