from . import bagofrequests as bag
from . import handlers
import pycurl
from . import result as res

class WebConsole(object):


    def __init__(self, url, **kwargs):

        def _handler_bundle_not_found(response, **kwargs):

            message = 'Bundle {0} not found'.format(kwargs['bundle_name'])
            result = res.PyAemResult(response)
            result.failure(message)
            return result

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            401: handlers.auth_fail,
            404: _handler_bundle_not_found,
            405: handlers.method_not_allowed
        }


    def start_bundle(self, bundle_name, **kwargs):

        def _handler_ok_start(response, **kwargs):

            message = 'Bundle {0} started'.format(kwargs['bundle_name'])
            result = res.PyAemResult(response)
            result.success(message)
            return result

        params = {
            'action': 'start'
        }

        _handlers = {
            200: _handler_ok_start,
            201: _handler_ok_start
        }

        opts = {
            'bundle_name': bundle_name
        }

        method = 'post'
        url = '{0}/system/console/bundles/{1}'.format(self.url, bundle_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = dict(self.kwargs.items() + opts.items())

        return bag.request(method, url, params, _handlers, **opts)


    def stop_bundle(self, bundle_name, **kwargs):

        def _handler_ok_stop(response, **kwargs):

            message = 'Bundle {0} stopped'.format(kwargs['bundle_name'])
            result = res.PyAemResult(response)
            result.success(message)
            return result

        params = {
            'action': 'stop'
        }

        _handlers = {
            200: _handler_ok_stop
        }

        opts = {
            'bundle_name': bundle_name
        }

        method = 'post'
        url = '{0}/system/console/bundles/{1}'.format(self.url, bundle_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = dict(self.kwargs.items() + opts.items())

        return bag.request(method, url, params, _handlers, **opts)


    def install_bundle(self, bundle_name, bundle_version, file_path, **kwargs):

        def _handler_ok_install(response, **kwargs):

            message = 'Bundle {0} installed'.format(kwargs['bundle_name'])
            result = res.PyAemResult(response)
            result.success(message)
            return result

        file_name = '{0}-{1}.jar'.format(bundle_name, bundle_version)

        params = {
            'action': 'install',
            'bundlefile': (pycurl.FORM_FILE, '{0}/{1}'.format(file_path.rstrip('/'), file_name))
        }

        _handlers = {
            200: _handler_ok_install,
            201: _handler_ok_install
        }

        opts = {
            'bundle_name': bundle_name
        }

        url = '{0}/system/console/bundles'.format(self.url)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = dict(self.kwargs.items() + opts.items())

        return bag.upload_file(url, params, _handlers, **opts)
