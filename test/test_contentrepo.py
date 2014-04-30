from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestContentRepo(unittest.TestCase):


    def test_init(self):

        content_repo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(content_repo.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(content_repo.kwargs['foo'], 'bar')

        self.assertTrue(401 in content_repo.handlers)
        self.assertTrue(405 in content_repo.handlers)


    def test_create_path(self):

        bag.request = MagicMock()
        content_repo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html')
        content_repo.create_path('/content/somepath', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html//content/somepath',
            {'foo': 'bar'},
            HandlersMatcher([200, 401, 405]))


if __name__ == '__main__':
    unittest.main()
    