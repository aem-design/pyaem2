from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestContentRepo(unittest.TestCase):


    def test_init(self):

        contentrepo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(contentrepo.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(contentrepo.kwargs['foo'], 'bar')

        self.assertTrue(401 in contentrepo.handlers)
        self.assertTrue(405 in contentrepo.handlers)


    def test_create_path(self):

        bag.request = MagicMock()
        contentrepo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html')
        contentrepo.create_path('/content/somepath', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html//content/somepath',
            {'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


if __name__ == '__main__':
    unittest.main()
    