from mock import MagicMock
import pyaem
from pyaem import bagofrequests as bag
import unittest
from .util import HandlersMatcher

class TestContentRepo(unittest.TestCase):


    def setUp(self):

        self.content_repo = pyaem.contentrepo.ContentRepo('http://localhost:4502', debug=True)
        bag.request = MagicMock()

    def test_init(self):

        self.assertEqual(self.content_repo.url, 'http://localhost:4502')
        self.assertEqual(self.content_repo.kwargs['debug'], True)

        self.assertTrue(401 in self.content_repo.handlers)
        self.assertTrue(405 in self.content_repo.handlers)


    def test_create_path(self):

        _self = self
        class CreatePathHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response, path='content/somepath')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Path content/somepath already existed')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response, path='content/somepath')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Path content/somepath created')
                _self.assertEquals(result.response, response)

                return super(CreatePathHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_path('content/somepath', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/content/somepath',
            {'foo': 'bar'},
            CreatePathHandlerMatcher([200, 201, 401, 405]),
            debug=True)


    def test_activate_path(self):

        _self = self
        class ActivatePathHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = {'body': ''}
                result = handlers[200](response, path='content/somepath')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Path content/somepath activated')
                _self.assertEquals(result.response, response)

                response = {'body': '<div class="error">some error</div>'}
                result = handlers[200](response, path='content/somepath')
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'some error')
                _self.assertEquals(result.response, response)

                return super(ActivatePathHandlerMatcher, self).__eq__(handlers)

        self.content_repo.activate_path('content/somepath', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/etc/replication/treeactivation.html',
            {'cmd': 'activate',
             'path': 'content/somepath',
             'foo': 'bar'},
            ActivatePathHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_create_user(self):

        _self = self
        class CreateUserHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'User home/users/someuser created')
                _self.assertEquals(result.response, response)

                response = {'body':
                    '<td><div id="Message">org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                    'User or Group for \'someuser\' already exists</div></td>'}
                result = handlers[500](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'User home/users/someuser already exists')
                _self.assertEquals(result.response, response)

                response = {'body': '<td><div id="Message">some other error message</div></td>'}
                result = handlers[500](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'some other error message')
                _self.assertEquals(result.response, response)

                return super(CreateUserHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_user('home/users', 'someuser', 'somepassword', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/libs/granite/security/post/authorizables',
            {'rep:password': 'somepassword',
             'intermediatePath': 'home/users',
             'authorizableId': 'someuser',
             'createUser': '',
             'foo': 'bar'},
            CreateUserHandlerMatcher([201, 401, 405, 500]),
            debug=True)


    def test_create_group(self):

        _self = self
        class CreateGroupHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Group home/groups/somegroup created')
                _self.assertEquals(result.response, response)

                result = handlers[500]({'body':
                    '<td><div id="Message">org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                    'User or Group for \'somegroup\' already exists</div></td>'})
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Group home/groups/somegroup already exists')

                result = handlers[500]({'body': '<td><div id="Message">some other error message</div></td>'})
                _self.assertEquals(result['status'], 'failure')
                _self.assertEquals(result['message'], 'some other error message')

                return super(CreateGroupHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_group('home/groups', 'somegroup', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/libs/granite/security/post/authorizables',
            {'profile/givenName': 'somegroup',
             'intermediatePath': 'home/groups',
             'authorizableId': 'somegroup',
             'createGroup': '',
             'foo': 'bar'},
            CreateGroupHandlerMatcher([201, 401, 405, 500]),
            debug=True)


    def test_change_password(self):

        _self = self
        class ChangePasswordHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                result = handlers[200](None)
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Password of user home/users/someuser was changed successfully')

                return super(ChangePasswordHandlerMatcher, self).__eq__(handlers)

        self.content_repo.change_password('home/users', 'someuser', 'someoldpassword', 'somenewpassword', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/home/users/someuser.rw.html',
            {':currentPassword': 'someoldpassword',
             'rep:password': 'somenewpassword',
             'foo': 'bar'},
            ChangePasswordHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_set_permission(self):

        _self = self
        class SetPermissionHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                result = handlers[200](None)
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'Permission of user someuser was set')

                return super(SetPermissionHandlerMatcher, self).__eq__(handlers)

        self.content_repo.set_permission('someuser', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html',
            {'authorizableId': 'someuser',
             'foo': 'bar'},
            SetPermissionHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_delete_agent(self):

        _self = self
        class DeleteAgentHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                result = handlers[204](None)
                _self.assertEquals(result['status'], 'success')
                _self.assertEquals(result['message'], 'author agent someagent was deleted')

                result = handlers[404](None)
                _self.assertEquals(result['status'], 'warning')
                _self.assertEquals(result['message'], 'author agent someagent not found')

                return super(DeleteAgentHandlerMatcher, self).__eq__(handlers)

        self.content_repo.delete_agent('someagent', 'author', foo='bar')
        bag.request.assert_called_once_with(
            'delete',
            'http://localhost:4502/etc/replication/agents.author/someagent',
            {'foo': 'bar'},
            DeleteAgentHandlerMatcher([204, 402, 405]),
            debug=True)


if __name__ == '__main__':
    unittest.main()
    