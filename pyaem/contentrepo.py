from . import bagofrequests as bag
from BeautifulSoup import BeautifulSoup
from . import handlers
import re
from . import result as res

HEX_MASSAGE = [(re.compile('&#x([^;]+);'), lambda m: '&#%d;' % int(m.group(1), 16))]

class ContentRepo(object):


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
            result = res.PyAemResult(response)
            result.warning(message)
            return result

        def _handler_ok(response, **kwargs):

            message = 'Path {0} created'.format(path)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        _handlers = {
            200: _handler_exist,
            201: _handler_ok
        }

        method = 'post'
        url = '{0}/{1}'.format(self.url, path)
        params = kwargs
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def activate_path(self, path, **kwargs):

        def _handler_ok(response, **kwargs):

            soup = BeautifulSoup(response['body'],
                convertEntities=BeautifulSoup.HTML_ENTITIES,
                markupMassage=HEX_MASSAGE
            )
            errors = soup.findAll(attrs={'class': 'error'})

            result = res.PyAemResult(response)
            if len(errors) == 0:
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
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def create_user(self, user_path, user_name, password, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'User {0}/{1} created'.format(user_path, user_name)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        def _handler_exist_or_error(response, **kwargs):

            soup = BeautifulSoup(response['body'],
                convertEntities=BeautifulSoup.HTML_ENTITIES,
                markupMassage=HEX_MASSAGE
            )
            message_elem = soup.find('div', {'id': 'Message'})
            if message_elem != None:
                message = message_elem.contents[0]

            exist_message = ('org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                'User or Group for \'{0}\' already exists'.format(user_name))

            result = res.PyAemResult(response)
            if message == exist_message:
                result.warning('User {0}/{1} already exists'.format(user_path, user_name))
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
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def add_user_to_group(self, user_name, group_path, group_name, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'User {0} added to group {1}/{2}'.format(user_name, group_path, group_name)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        params = {
            'addMembers': user_name
        }

        _handlers = {
            200: _handler_ok
        }

        method = 'post'
        url = '{0}/{1}/{2}.rw.html'.format(self.url, group_path, group_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def create_group(self, group_path, group_name, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'Group {0}/{1} created'.format(group_path, group_name)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        def _handler_exist_or_error(response, **kwargs):

            soup = BeautifulSoup(response['body'],
                convertEntities=BeautifulSoup.HTML_ENTITIES,
                markupMassage=HEX_MASSAGE
            )
            message_elem = soup.find('div', {'id': 'Message'})
            if message_elem != None:
                message = message_elem.contents[0]

            exist_message = ('org.apache.jackrabbit.api.security.user.AuthorizableExistsException: ' +
                'User or Group for \'{0}\' already exists'.format(group_name))

            result = res.PyAemResult(response)
            if message == exist_message:
                result.warning('Group {0}/{1} already exists'.format(group_path, group_name))
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
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def change_password(self, user_path, user_name, old_password, new_password, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'Password of user {0}/{1} was changed successfully'.format(user_path, user_name)
            result = res.PyAemResult(response)
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
        url = '{0}/{1}/{2}.rw.html'.format(self.url, user_path, user_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def set_permission(self, user_or_group_name, path, permissions, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'Permissions {0} set on path {1} for user/group {2}'.format(permissions, path, user_or_group_name)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        def _handler_not_found(response, **kwargs):

            soup = BeautifulSoup(response['body'],
                convertEntities=BeautifulSoup.HTML_ENTITIES,
                markupMassage=HEX_MASSAGE
            )
            message_elem = soup.find('div', {'id': 'Message'})
            message = message_elem.contents[0]

            result = res.PyAemResult(response)
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
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def set_agent(self, agent_name, run_mode, **kwargs):

        def _handler_ok(response, **kwargs):

            message = '{0} agent {1} set'.format(run_mode, agent_name)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        params = {
        }

        _handlers = {
            200: _handler_ok
        }

        method = 'post'
        url = '{0}/etc/replication/agents.{1}/{2}'.format(self.url, run_mode, agent_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def delete_agent(self, agent_name, run_mode, **kwargs):

        def _handler_ok(response, **kwargs):

            message = '{0} agent {1} deleted'.format(run_mode, agent_name)
            result = res.PyAemResult(response)
            result.success(message)
            return result

        def _handler_not_found(response, **kwargs):

            message = '{0} agent {1} not found'.format(run_mode, agent_name)
            result = res.PyAemResult(response)
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
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
