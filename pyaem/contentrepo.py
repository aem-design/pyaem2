import bagofrequests as bag
from BeautifulSoup import *
import handlers
import json
import re

class ContentRepo(object):


    def __init__(self, url, **kwargs):

        self.url      = url
        self.kwargs   = kwargs
        self.handlers = {
            401: handlers.auth_fail,
            405: handlers.method_not_allowed
        }


    def create_path(self, path, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'Path {0} was created'.format(path)
            }

            return result

        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/{1}'.format(self.url, path)
        params    = kwargs
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def activate_path(self, path, **kwargs):

        def _handler_ok(response, **kwargs):

            HEX_MASSAGE = [(re.compile('&#x([^;]+);'), lambda m: '&#%d;' % int(m.group(1), 16))]

            code   = response['http_code']
            soup   = BeautifulSoup(response['body'],
                convertEntities = BeautifulSoup.HTML_ENTITIES,
                markupMassage   = HEX_MASSAGE
            )
            errors = soup.findAll(attrs={ 'class': 'error' })

            if len(errors) == 0:
                result = {
                    'status' : 'success',
                    'message': 'Path was successfully activated'
                }
            else:
                result = {
                    'status' : 'failure',
                    'message': errors[0].string
                }

            return result

        params    = {
            'cmd' : 'activate',
            'path': path
        }
        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/etc/replication/treeactivation.html'.format(self.url)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def create_user(self, user_path, user_name, password, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'User {0}/{1} was created'.format(user_path, user_name)
            }

            return result

        def _handler_exist_or_error(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'User {0}/{1} already exists or there is an unexpected error - check AEM log'
                    .format(user_path, user_name)
            }

            return result

        params    = {
            'createUser'      : '',
            'authorizableId'  : user_name,
            'rep:password'    : password,
            'intermediatePath': user_path
        }
        _handlers = {
            201: _handler_ok,
            500: _handler_exist_or_error
        }
        method    = 'post'
        url       = '{0}/libs/granite/security/post/authorizables'.format(self.url)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def add_user_to_group(self, user_name, group_path, group_name, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'User {0} was added to group {1}/{2}'.format(user_name, group_path, group_name)
            }

            return result

        params    = {
            'addMembers': user_name
        }
        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/{1}/{2}.rw.html'.format(self.url, group_path, group_name)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)

        
    def create_group(self, group_path, group_name, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'Group {0}/{1} was created'.format(group_path, group_name)
            }

            return result

        params    = {
            'createGroup'     : '',
            'authorizableId'  : group_name,
            'profile/giveName': group_name,
            'intermediatePath': group_path
        }
        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/libs/granite/security/post/authorizables'.format(self.url)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def change_password(self, user_path, old_password, new_password, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'Password of user {0} was changed successfully'.format(user_path)
            }

            return result

        params    = {
            ':currentPassword': old_password,
            'rep:password'    : new_password
        }
        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/home/users/{1}.rw.html'.format(self.url, user_path)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def set_permission(self, user_name, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'Permission of user {0} was set'.format(user_name)
            }

            return result

        params    = {
            'authorizableId': user_name
        }
        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/.cqactions.html'.format(self.url)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def set_agent(self, agent_name, run_mode, **kwargs):

        def _handler_ok(response, **kwargs):

            result = {
                'status' : 'success',
                'message': '{0} agent {1} was set'.format(run_mode, agent_name)
            }

            return result

        params    = {
        }
        _handlers = {
            200: _handler_ok
        }
        method    = 'post'
        url       = '{0}/etc/replication/agents.{1}/{2}'.format(self.url, run_mode, agent_name)
        params    = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts      = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
