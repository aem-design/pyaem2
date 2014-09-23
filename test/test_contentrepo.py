from mock import MagicMock
import pyaem
import json
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
                result = handlers[200](response, path='/content/somepath/')
                _self.assertEquals(result.is_warning(), True)
                _self.assertEquals(result.message, 'Path /content/somepath/ already exists')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response, path='/content/somepath/')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Path /content/somepath/ created')
                _self.assertEquals(result.response, response)

                return super(CreatePathHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_path('/content/somepath/', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/content/somepath/',
            {'foo': 'bar'},
            CreatePathHandlerMatcher([200, 201, 401, 405]),
            debug=True)


    def test_delete_path(self):

        _self = self
        class DeletePathHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[204](response, path='/content/somepath/')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Path /content/somepath/ deleted')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[404](response, path='/content/somepath/')
                _self.assertEquals(result.is_warning(), True)
                _self.assertEquals(result.message, 'Path /content/somepath/ not found')
                _self.assertEquals(result.response, response)

                return super(DeletePathHandlerMatcher, self).__eq__(handlers)

        self.content_repo.delete_path('/content/somepath/', foo='bar')
        bag.request.assert_called_once_with(
            'delete',
            'http://localhost:4502/content/somepath/',
            {'foo': 'bar'},
            DeletePathHandlerMatcher([204, 404]),
            debug=True)


    def test_activate_path(self):

        _self = self
        class ActivatePathHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = {'body': ''}
                result = handlers[200](response, path='/content/somepath/')
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Path /content/somepath/ activated')
                _self.assertEquals(result.response, response)

                response = {'body': '<div class="error">some error</div>'}
                result = handlers[200](response, path='/content/somepath/')
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'some error')
                _self.assertEquals(result.response, response)

                return super(ActivatePathHandlerMatcher, self).__eq__(handlers)

        self.content_repo.activate_path('/content/somepath/', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/etc/replication/treeactivation.html',
            {'cmd': 'activate',
             'path': '/content/somepath/',
             'foo': 'bar'},
            ActivatePathHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_does_user_exist(self):

        _self = self
        class DoesUserExistHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'User /home/users/someuser exists')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[404](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'User /home/users/someuser does not exist')
                _self.assertEquals(result.response, response)

                return super(DoesUserExistHandlerMatcher, self).__eq__(handlers)

        self.content_repo.does_user_exist('/home/users/', 'someuser', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/home/users/someuser',
            {'foo': 'bar'},
            DoesUserExistHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_create_user(self):

        _self = self
        class CreateUserHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'User /home/users/someuser created')
                _self.assertEquals(result.response, response)

                response = {'body':
                    '<td><div id="Message">org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                    'User or Group for \'someuser\' already exists</div></td>'}
                result = handlers[500](response)
                _self.assertEquals(result.is_warning(), True)
                _self.assertEquals(result.message, 'User /home/users/someuser already exists')
                _self.assertEquals(result.response, response)

                response = {'body': '<td><div id="Message">some other error message</div></td>'}
                result = handlers[500](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'some other error message')
                _self.assertEquals(result.response, response)

                return super(CreateUserHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_user('/home/users/', 'someuser', 'somepassword', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/libs/granite/security/post/authorizables',
            {'rep:password': 'somepassword',
             'intermediatePath': '/home/users/',
             'authorizableId': 'someuser',
             'createUser': '',
             'foo': 'bar'},
            CreateUserHandlerMatcher([201, 401, 405, 500]),
            debug=True)


    def test_add_user_to_group(self):

        _self = self
        class AddUserToGroupHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'User someuser added to group /home/groups/somegroup')
                _self.assertEquals(result.response, response)

                return super(AddUserToGroupHandlerMatcher, self).__eq__(handlers)

        self.content_repo.add_user_to_group('someuser', '/home/groups/', 'somegroup', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/home/groups/somegroup.rw.html',
            {'addMembers': 'someuser',
             'foo': 'bar'},
            AddUserToGroupHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_does_group_exist(self):

        _self = self
        class DoesGroupExistHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Group /home/groups/somegroup exists')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[404](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'Group /home/groups/somegroup does not exist')
                _self.assertEquals(result.response, response)

                return super(DoesGroupExistHandlerMatcher, self).__eq__(handlers)

        self.content_repo.does_group_exist('/home/groups/', 'somegroup', foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/home/groups/somegroup',
            {'foo': 'bar'},
            DoesGroupExistHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_create_group(self):

        _self = self
        class CreateGroupHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Group /home/groups/somegroup created')
                _self.assertEquals(result.response, response)

                response = {'body':
                    '<td><div id="Message">org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                    'User or Group for \'somegroup\' already exists</div></td>'}
                result = handlers[500](response)
                _self.assertEquals(result.is_warning(), True)
                _self.assertEquals(result.message, 'Group /home/groups/somegroup already exists')
                _self.assertEquals(result.response, response)

                response = {'body': '<td><div id="Message">some other error message</div></td>'}
                result = handlers[500](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'some other error message')
                _self.assertEquals(result.response, response)

                return super(CreateGroupHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_group('/home/groups/', 'somegroup', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/libs/granite/security/post/authorizables',
            {'profile/givenName': 'somegroup',
             'intermediatePath': '/home/groups/',
             'authorizableId': 'somegroup',
             'createGroup': '',
             'foo': 'bar'},
            CreateGroupHandlerMatcher([201, 401, 405, 500]),
            debug=True)


    def test_change_password(self):

        _self = self
        class ChangePasswordHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'User /home/users/someuser password changed')
                _self.assertEquals(result.response, response)

                return super(ChangePasswordHandlerMatcher, self).__eq__(handlers)

        self.content_repo.change_password('/home/users/', 'someuser', 'someoldpassword', 'somenewpassword', foo='bar')
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

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message,
                    'Permissions read:true,modify:true set on path somepath for user/group somegroup')
                _self.assertEquals(result.response, response)

                response = {'body': '<td><div id="Message">No such node /home/groups/somegroup</div></td>'}
                result = handlers[404](response)
                _self.assertEquals(result.is_failure(), True)
                _self.assertEquals(result.message, 'No such node /home/groups/somegroup')
                _self.assertEquals(result.response, response)

                return super(SetPermissionHandlerMatcher, self).__eq__(handlers)

        self.content_repo.set_permission('somegroup', 'somepath', 'read:true,modify:true', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/.cqactions.html',
            {'authorizableId': 'somegroup',
             'changelog': 'path:somepath,read:true,modify:true',
             'foo': 'bar'},
            SetPermissionHandlerMatcher([200, 401, 405]),
            debug=True)


    def test_create_flush_agent(self):

        _self = self
        class SetAgentHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'publish agent someagent updated')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'publish agent someagent created')
                _self.assertEquals(result.response, response)

                return super(SetAgentHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_agent(
            'someagent', 'flush', None, None, 'http://somehost:8080', 'publish', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/etc/replication/agents.publish/someagent',
            {'jcr:content/serializationType': 'flush',
             'jcr:content/noVersioning': 'true',
             'jcr:primaryType': 'cq:Page',
             'jcr:content/transportUri': 'http://somehost:8080/dispatcher/invalidate.cache',
             'jcr:content/enabled': 'true',
             'jcr:content/jcr:mixinTypes': 'cq:ReplicationStatus',
             'jcr:content/cq:template': '/libs/cq/replication/templates/agent',
             'jcr:content/cq:name': 'flush',
             'jcr:content/triggerSpecific': 'true',
             'jcr:content/protocolHTTPMethod': 'GET',
             'jcr:content/protocolHTTPHeaders@TypeHint': 'String[]',
             'jcr:content/triggerReceive': 'true',
             'jcr:content/protocolHTTPHeaders': ['CQ-Action:{action}', 'CQ-Handle:{path}', 'CQ-Path:{path}'],
             'jcr:content/sling:resourceType': '/libs/cq/replication/components/agent',
             'foo': 'bar'},
            SetAgentHandlerMatcher([201, 204, 402, 405]),
            debug=True)


    def test_create_replicate_agent(self):

        _self = self
        class SetAgentHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'author agent someagent updated')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'author agent someagent created')
                _self.assertEquals(result.response, response)

                return super(SetAgentHandlerMatcher, self).__eq__(handlers)

        self.content_repo.create_agent(
            'someagent', 'replicate', 'someuser', 'somepassword', 'http://somehost:8080', 'author', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/etc/replication/agents.author/someagent',
            {'jcr:content/serializationType': 'durbo',
             'jcr:primaryType': 'cq:Page',
             'jcr:content/transportUri': 'http://somehost:8080/bin/receive?sling:authRequestLogin=1',
             'jcr:content/enabled': 'true',
             'jcr:content/transportUser': 'someuser',
             'jcr:content/cq:template': '/libs/cq/replication/templates/agent',
             'jcr:content/transportPassword': 'somepassword',
             'jcr:content/sling:resourceType': '/libs/cq/replication/components/agent',
             'foo': 'bar'},
            SetAgentHandlerMatcher([201, 204, 402, 405]),
            debug=True)


    def test_delete_agent(self):

        _self = self
        class DeleteAgentHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[204](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'author agent someagent deleted')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[404](response)
                _self.assertEquals(result.is_warning(), True)
                _self.assertEquals(result.message, 'author agent someagent not found')
                _self.assertEquals(result.response, response)

                return super(DeleteAgentHandlerMatcher, self).__eq__(handlers)

        self.content_repo.delete_agent('someagent', 'author', foo='bar')
        bag.request.assert_called_once_with(
            'delete',
            'http://localhost:4502/etc/replication/agents.author/someagent',
            {'foo': 'bar'},
            DeleteAgentHandlerMatcher([204, 402, 405]),
            debug=True)


    def test_set_property(self):

        _self = self
        class SetPropertyHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Set property sling:target=/welcome.html on path /content/mysite')
                _self.assertEquals(result.response, response)

                response = None
                result = handlers[201](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Set property sling:target=/welcome.html on path /content/mysite')
                _self.assertEquals(result.response, response)

                return super(SetPropertyHandlerMatcher, self).__eq__(handlers)

        self.content_repo.set_property('/content/mysite', 'sling:target', '/welcome.html', foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/content/mysite',
            {'sling:target': '/welcome.html', 'foo': 'bar'},
            SetPropertyHandlerMatcher([200, 201, 405]),
            debug=True)


    def test_enable_workflow(self):

        _self = self
        class EnableWorkflowHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message,
                    'Workflow /etc/workflow/models/dam/update_asset/jcr:content/model enabled')
                _self.assertEquals(result.response, response)

                return super(EnableWorkflowHandlerMatcher, self).__eq__(handlers)

        self.content_repo.enable_workflow(
            '/etc/workflow/models/dam/update_asset/jcr:content/model',
            '/content/dam(/.*/)renditions/original',
            '/etc/workflow/launcher/config/update_asset_mod',
            'nt:file',
            'author',
            foo='bar')
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/libs/cq/workflow/launcher',
            {
                ':status': 'browser',
                '_charset_': 'utf-8',
                'condition': '',
                'description': '',
                'edit': '/etc/workflow/launcher/config/update_asset_mod',
                'enabled': 'true',
                'eventType': '16',
                'excludeList': '',
                'glob': '/content/dam(/.*/)renditions/original',
                'nodetype': 'nt:file',
                'runModes': 'author',
                'workflow': '/etc/workflow/models/dam/update_asset/jcr:content/model',
                'foo': 'bar'
            },
            EnableWorkflowHandlerMatcher([200, 201, 405]),
            debug=True)


    def test_disable_workflow(self):

        _self = self
        class DisableWorkflowHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                response = None
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message,
                    'Workflow /etc/workflow/models/dam/update_asset/jcr:content/model disabled')
                _self.assertEquals(result.response, response)

                return super(DisableWorkflowHandlerMatcher, self).__eq__(handlers)

        self.content_repo.disable_workflow(
            '/etc/workflow/models/dam/update_asset/jcr:content/model',
            '/content/dam(/.*/)renditions/original',
            '/etc/workflow/launcher/config/update_asset_mod',
            'nt:file',
            'author',
            foo='bar',
            condition='Some condition',
            description='Work flow for nested metadata nodes',
            excludeList='jcr:lastModified,dc:modified,dc:format,jcr:lastModifiedBy,newRendition'
            )
        bag.request.assert_called_once_with(
            'post',
            'http://localhost:4502/libs/cq/workflow/launcher',
            {
                ':status': 'browser',
                '_charset_': 'utf-8',
                'condition': 'Some condition',
                'description': 'Work flow for nested metadata nodes',
                'edit': '/etc/workflow/launcher/config/update_asset_mod',
                'enabled': 'false',
                'eventType': '16',
                'excludeList': 'jcr:lastModified,dc:modified,dc:format,jcr:lastModifiedBy,newRendition',
                'glob': '/content/dam(/.*/)renditions/original',
                'nodetype': 'nt:file',
                'runModes': 'author',
                'workflow': '/etc/workflow/models/dam/update_asset/jcr:content/model',
                'foo': 'bar'
            },
            DisableWorkflowHandlerMatcher([200, 201, 405]),
            debug=True)


    def test_get_cluster_list(self):

        _self = self
        class GetClusterListHandlerMatcher(HandlersMatcher):
            def __eq__(self, handlers):

                cluster_list = {
                    'masterId':'node-id-2',
                    'nodeId':'node-id-1',
                    'nodes':[
                        {'OS':'Linux', 'hostname':'host-1.com', 'id':'node-id-1', 'repositoryHome':'/path/to/repo'},
                        {'OS':'Linux', 'hostname':'host-2.com', 'id':'node-id-2', 'repositoryHome':'/path/to/repo'}
                    ]}

                response = {'body': json.dumps(cluster_list)}
                result = handlers[200](response)
                _self.assertEquals(result.is_success(), True)
                _self.assertEquals(result.message, 'Cluster list retrieved')

                data = json.loads(result.response['body'])
                _self.assertEquals(data['masterId'], 'node-id-2')
                _self.assertEquals(data['nodeId'], 'node-id-1')
                _self.assertEquals(len(data['nodes']), 2)
                _self.assertEquals(data['nodes'][0]['OS'], 'Linux')
                _self.assertEquals(data['nodes'][0]['hostname'], 'host-1.com')
                _self.assertEquals(data['nodes'][0]['id'], 'node-id-1')
                _self.assertEquals(data['nodes'][1]['OS'], 'Linux')
                _self.assertEquals(data['nodes'][1]['hostname'], 'host-2.com')
                _self.assertEquals(data['nodes'][1]['id'], 'node-id-2')

                _self.assertEquals(result.response, response)

                return super(GetClusterListHandlerMatcher, self).__eq__(handlers)

        self.content_repo.get_cluster_list(foo='bar')
        bag.request.assert_called_once_with(
            'get',
            'http://localhost:4502/libs/granite/cluster/content/admin/cluster.list.json',
            {'foo': 'bar'},
            GetClusterListHandlerMatcher([200]),
            debug=True)


if __name__ == '__main__':
    unittest.main()
    