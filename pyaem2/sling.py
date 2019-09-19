from . import bagofrequests as bag
from . import handlers
from . import result as res

class Sling():


    def __init__(self, url, **kwargs):

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            401: handlers.auth_fail
        }


    def is_valid_login(self, **kwargs):

        def _handler_valid(response, **kwargs):

            message = 'Login is valid'
            result = res.PyAem2Result(response)
            result.success(message)
            return result

        def _handler_invalid(response, **kwargs):

            message = 'Login is invalid'
            result = res.PyAem2Result(response)
            result.failure(message)
            return result

        _handlers = {
            200: _handler_valid,
            401: _handler_invalid
        }

        method = 'get'
        url = '{0}/system/sling/login'.format(self.url)
        params = kwargs
        handlers_all = dict(self.handlers.items()).copy()
        handlers_all.update(dict(_handlers.items()))
        opts = self.kwargs

        return bag.request(method, url, params, handlers_all, **opts)
