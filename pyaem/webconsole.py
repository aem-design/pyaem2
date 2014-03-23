import bagofrequests as bag
import handlers

class WebConsole(object):


  def __init__(self, url, **kwargs):

    def _handler_bundle_not_found(response, **kwargs):

      result = {
        'status' : 'failure',
        'message': 'Bundle {0} not found'.format(kwargs['bundle_name'])
      }
      return result

    self.url      = url
    self.kwargs   = kwargs
    self.handlers = {
      401: handlers.auth_fail,
      404: _handler_bundle_not_found,
      405: handlers.method_not_allowed
    }


  def start_bundle(self, bundle_name, **kwargs):

    def _handler_ok(response, **kwargs):
      result = {
        'status' : 'success',
        'message': 'Bundle {0} was successfully started'.format(kwargs['bundle_name'])
      }
      return result

    params    = {
      'action': 'start'
    }
    _handlers = {
      200: _handler_ok
    }
    opts      = {
      'bundle_name': bundle_name
    }
    method    = 'post'
    url       = '{0}/system/console/bundles/{1}'.format(self.url, bundle_name)
    params    = dict(params.items() + kwargs.items())
    _handlers = dict(self.handlers.items() + _handlers.items())
    opts      = dict(self.kwargs.items() + opts.items())

    return bag.request(method, url, params, _handlers, **opts)


  def stop_bundle(self, bundle_name, **kwargs):

    def _handler_ok(response, **kwargs):
      result = {
        'status' : 'success',
        'message': 'Bundle {0} was successfully stopped'.format(kwargs['bundle_name'])
      }
      return result

    params    = {
      'action': 'stop'
    }
    _handlers = {
      200: _handler_ok
    }
    opts      = {
      'bundle_name': bundle_name
    }
    method    = 'post'
    url       = '{0}/system/console/bundles/{1}'.format(self.url, bundle_name)
    params    = dict(params.items() + kwargs.items())
    _handlers = dict(self.handlers.items() + _handlers.items())
    opts      = dict(self.kwargs.items() + opts.items())

    return bag.request(method, url, params, _handlers, **opts)