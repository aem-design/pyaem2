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

        _self = self
        class CreatePathHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                result = handlers[200](None, path='content/somepath')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Path content/somepath already existed')

                result = handlers[201](None, path='content/somepath')
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Path content/somepath was created')

                return handlers.keys() == self.handler_keys

        bag.request = MagicMock()
        content_repo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html')
        content_repo.create_path('content/somepath', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/content/somepath',
            {'foo': 'bar'},
            CreatePathHandlerMatcher([200, 401, 405, 201]))


    def test_change_password(self):

        _self = self
        class ChangePasswordHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):
                result = handlers[200](None)
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Password of user home/users/someuser was changed successfully')
                return handlers.keys() == self.handler_keys

        bag.request = MagicMock()
        content_repo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html')
        content_repo.change_password('home/users', 'someuser', 'someoldpassword', 'somenewpassword', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html/home/users/someuser.rw.html',
            {':currentPassword': 'someoldpassword',
             'rep:password': 'somenewpassword',
             'foo': 'bar'},
            ChangePasswordHandlerMatcher([200, 401, 405]))


if __name__ == '__main__':
    unittest.main()
    