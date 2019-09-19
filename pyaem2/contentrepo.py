import re
from bs4 import BeautifulSoup
from . import bagofrequests as bag
from . import handlers
from . import result as res

HEX_MASSAGE = [(re.compile('&#x([^;]+);'), lambda m: '&#%d;' % int(m.group(1), 16))]


class ContentRepo():
    def __init__(self, url, **kwargs):

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            401: handlers.auth_fail,
            405: handlers.method_not_allowed
        }

    def create_path(self, path, **kwargs):

        def _handler_exist(response, **kwargs):
            message = 'Path {0} already exists'.format(path)
            result = res.PyAem2Result(response)
            result.warning(message)
            return result

        def _handler_ok(response, **kwargs):
            message = 'Path {0} created'.format(path)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        _handlers = {
            200: _handler_exist,
            201: _handler_ok
        }

        method = 'post'
        url = '{0}/{1}'.format(self.url, path.lstrip('/'))
        params = kwargs
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params, handlers_all, **opts)

    def delete_path(self, path, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'Path {0} deleted'.format(path)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_not_found(response, **kwargs):
            message = 'Path {0} not found'.format(path)
            result = res.PyAem2Result(response)
            result.warning(message)
            return result

        _handlers = {
            204: _handler_ok,
            404: _handler_not_found
        }

        method = 'delete'
        url = '{0}/{1}'.format(self.url, path.lstrip('/'))
        params = kwargs
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params, handlers_all, **opts)

    def activate_path(self, path, **kwargs):

        def _handler_ok(response, **kwargs):

            soup = BeautifulSoup(response['body'], 'html.parser')
            errors = soup.find_all(class_="error")

            result = res.PyAem2Result(response)
            if not errors:
                message = 'Path {0} activated'.format(path)
                result.success(message)
            else:
                message = errors[0].string
                result.failure(message)
            return result

        params = {
            'cmd': 'activate',
            'path': path
        }

        _handlers = {
            200: _handler_ok
        }

        method = 'post'
        url = '{0}/etc/replication/treeactivation.html'.format(self.url)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def does_user_exist(self, user_path, user_name, **kwargs):

        node_path = '{0}/{1}'.format(user_path.rstrip('/'), user_name.lstrip('/'))
        return self._does_node_exist(node_path, 'User', **kwargs)

    def create_user(self, user_path, user_name, password, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'User {0}/{1} created'.format(user_path.rstrip('/'), user_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_exist_or_error(response, **kwargs):

            soup = BeautifulSoup(response['body'], 'html.parser')
            message_elem = soup.find('div', {'id': 'Message'})
            if message_elem is not None:
                message = message_elem.contents[0]

            exist_message = ('org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                             'User or Group for \'{0}\' already exists'.format(user_name))

            result = res.PyAem2Result(response)
            if message == exist_message:
                result.warning('User {0}/{1} already exists'.format(user_path.rstrip('/'), user_name))
            else:
                result.failure(message)
            return result

        params = {
            'createUser': '',
            'authorizableId': user_name,
            'rep:password': password,
            'intermediatePath': user_path
        }

        _handlers = {
            201: _handler_ok,
            500: _handler_exist_or_error
        }

        method = 'post'
        url = '{0}/libs/granite/security/post/authorizables'.format(self.url)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def add_user_to_group(self, user_name, group_path, group_name, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'User {0} added to group {1}/{2}'.format(user_name, group_path.rstrip('/'), group_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        params = {
            'addMembers': user_name
        }

        _handlers = {
            200: _handler_ok
        }

        method = 'post'
        url = '{0}/{1}/{2}.rw.html'.format(self.url, group_path.strip('/'), group_name)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def does_group_exist(self, group_path, group_name, **kwargs):

        node_path = '{0}/{1}'.format(group_path.rstrip('/'), group_name.lstrip('/'))
        return self._does_node_exist(node_path, 'Group', **kwargs)

    def create_group(self, group_path, group_name, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'Group {0}/{1} created'.format(group_path.rstrip('/'), group_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_exist_or_error(response, **kwargs):

            soup = BeautifulSoup(response['body'], 'html.parser')
            message_elem = soup.find('div', {'id': 'Message'})
            if message_elem is not None:
                message = message_elem.contents[0]

            exist_message = ('org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                             'User or Group for \'{0}\' already exists'.format(group_name))

            result = res.PyAem2Result(response)
            if message == exist_message:
                result.warning('Group {0}/{1} already exists'.format(group_path.rstrip('/'), group_name))
            else:
                result.failure(message)
            return result

        params = {
            'createGroup': '',
            'authorizableId': group_name,
            'profile/givenName': group_name,
            'intermediatePath': group_path
        }

        _handlers = {
            201: _handler_ok,
            500: _handler_exist_or_error
        }

        method = 'post'
        url = '{0}/libs/granite/security/post/authorizables'.format(self.url)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def change_password(self, user_path, user_name, old_password, new_password, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'User {0}/{1} password changed'.format(user_path.rstrip('/'), user_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        params = {
            ':currentPassword': old_password,
            'rep:password': new_password
        }

        _handlers = {
            200: _handler_ok
        }

        method = 'post'
        url = '{0}/{1}/{2}.rw.html'.format(self.url, user_path.strip('/'), user_name)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def set_permission(self, user_or_group_name, path, permissions, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'Permissions {0} set on path {1} for user/group {2}'.format(permissions, path, user_or_group_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_not_found(response, **kwargs):
            soup = BeautifulSoup(response['body'], 'html.parser')
            message_elem = soup.find('div', {'id': 'Message'})
            message = message_elem.contents[0]

            result = res.PyAem2Result(response)
            result.failure(message)
            return result

        params = {
            'authorizableId': user_or_group_name,
            'changelog': 'path:{0},{1}'.format(path, permissions)
        }

        _handlers = {
            200: _handler_ok,
            404: _handler_not_found
        }

        method = 'post'
        url = '{0}/.cqactions.html'.format(self.url)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def create_agent(self, agent_name, agent_type, dest_username, dest_password, dest_url, run_mode, **kwargs):

        def _handler_ok_created(response, **kwargs):

            message = '{0} agent {1} created'.format(run_mode, agent_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_ok_updated(response, **kwargs):

            message = '{0} agent {1} updated'.format(run_mode, agent_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        if agent_type == 'flush':
            params = {
                'jcr:content/cq:name': 'flush',
                'jcr:content/protocolHTTPHeaders': ['CQ-Action:{action}', 'CQ-Handle:{path}', 'CQ-Path:{path}'],
                'jcr:content/protocolHTTPHeaders@TypeHint': 'String[]',
                'jcr:content/protocolHTTPMethod': 'GET',
                'jcr:content/serializationType': 'flush',
                'jcr:content/noVersioning': 'true',
                'jcr:content/jcr:mixinTypes': 'cq:ReplicationStatus',
                'jcr:content/triggerReceive': 'true',
                'jcr:content/triggerSpecific': 'true',
                'jcr:content/transportUri': '{0}/dispatcher/invalidate.cache'.format(dest_url.rstrip('/'))
            }
        else:
            params = {
                'jcr:content/serializationType': 'durbo',
                'jcr:content/transportUri': '{0}/bin/receive?sling:authRequestLogin=1'.format(dest_url.rstrip('/'))
            }

        params['jcr:primaryType'] = 'cq:Page'
        params['jcr:content/sling:resourceType'] = '/libs/cq/replication/components/agent'
        params['jcr:content/cq:template'] = '/libs/cq/replication/templates/agent'
        params['jcr:content/enabled'] = 'true'

        if dest_username is not None:
            params['jcr:content/transportUser'] = dest_username
        if dest_password is not None:
            params['jcr:content/transportPassword'] = dest_password

        _handlers = {
            200: _handler_ok_updated,
            201: _handler_ok_created
        }

        method = 'post'
        url = '{0}/etc/replication/agents.{1}/{2}'.format(self.url, run_mode, agent_name)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def delete_agent(self, agent_name, run_mode, **kwargs):

        def _handler_ok(response, **kwargs):
            message = '{0} agent {1} deleted'.format(run_mode, agent_name)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_not_found(response, **kwargs):
            message = '{0} agent {1} not found'.format(run_mode, agent_name)
            result = res.PyAem2Result(response)
            result.warning(message)
            return result

        params = {
        }

        _handlers = {
            204: _handler_ok,
            404: _handler_not_found
        }

        method = 'delete'
        url = '{0}/etc/replication/agents.{1}/{2}'.format(self.url, run_mode, agent_name)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def set_property(self, path, property_name, property_value, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'Set property {0}={1} on path {2}'.format(property_name, property_value, path)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        params = {
            property_name: property_value
        }

        _handlers = {
            200: _handler_ok,
            201: _handler_ok
        }

        method = 'post'
        url = '{0}/{1}'.format(self.url, path.lstrip('/'))
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def enable_workflow(self, workflow, glob, edit, node_type, run_mode, **kwargs):

        return self._set_workflow(workflow, glob, edit, True, node_type, run_mode, **kwargs)

    def disable_workflow(self, workflow, glob, edit, node_type, run_mode, **kwargs):

        return self._set_workflow(workflow, glob, edit, False, node_type, run_mode, **kwargs)

    def _does_node_exist(self, node_path, node_desc, **kwargs):

        def _handler_ok(response, **kwargs):
            message = '{0} {1} exists'.format(node_desc, node_path)
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_not_found(response, **kwargs):
            message = '{0} {1} does not exist'.format(node_desc, node_path)
            result = res.PyAem2Result(response)
            result.failure(message)
            return result

        _handlers = {
            200: _handler_ok,
            404: _handler_not_found
        }

        method = 'get'
        url = '{0}/{1}'.format(self.url, node_path.lstrip('/'))
        params = kwargs
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params, handlers_all, **opts)

    def _set_workflow(self, workflow, glob, edit, is_enabled, node_type, run_mode, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'Workflow {0} {1}'.format(workflow, 'enabled' if is_enabled else 'disabled')
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        params = {
            ':status': 'browser',
            '_charset_': 'utf-8',
            'condition': kwargs.get('condition', ''),
            'description': kwargs.get('description', ''),
            'edit': edit,
            'enabled': 'true' if is_enabled else 'false',
            'eventType': '16',
            'excludeList': kwargs.get('excludeList', ''),
            'glob': glob,
            'nodetype': node_type,
            'runModes': run_mode,
            'workflow': workflow
        }

        _handlers = {
            200: _handler_ok
        }

        method = 'post'
        url = '{0}/libs/cq/workflow/launcher'.format(self.url)
        params_all = dict(params.items()).copy()
        params_all.update(dict(kwargs.items()))
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params_all, handlers_all, **opts)

    def get_cluster_list(self, **kwargs):

        def _handler_ok(response, **kwargs):
            message = 'Cluster list retrieved'
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        _handlers = {
            200: _handler_ok
        }

        method = 'get'
        url = '{0}/libs/granite/cluster/content/admin/cluster.list.json'.format(self.url)
        params = kwargs
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params, handlers_all, **opts)
