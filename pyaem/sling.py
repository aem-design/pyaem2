from . import bagofrequests as bag
from . import handlers
from . import result as res

class Sling(object):


    def __init__(self, url, **kwargs):

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            401: handlers.auth_fail
        }


    def is_valid_login(self, **kwargs):

        def _handler_valid(response, **kwargs):

            message = 'Login is valid'
            result = res.PyAemResult(response)
            result.success(message)
            return result

        def _handler_invalid(response, **kwargs):

            message = 'Login is invalid'
            result = res.PyAemResult(response)
            result.failure(message)
            return result

        _handlers = {
            200: _handler_valid,
            401: _handler_invalid
        }

        method = 'get'
        url = '{0}/system/sling/login'.format(self.url)
        params = kwargs
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
