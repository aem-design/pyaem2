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


    def login(self, **kwargs):

        def _handler_ok(response, **kwargs):

            message = 'Login successfully'
            result = res.PyAemResult(response)
            result.success(message)
            return result

        _handlers = {
            200: _handler_ok
        }

        method = 'get'
        url = '{0}/sling/login'.format(self.url)
        params = kwargs
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
