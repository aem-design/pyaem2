from . import bagofrequests as bag
from . import handlers
import json
import pycurl
from . import result as res

class PackageManagerServiceJson(object):


    def __init__(self, url, **kwargs):

        def _handler_ok(response, **kwargs):

            data = json.loads(response['body'])
            message = data['msg']
            result = res.PyAemResult(response)

            if data['success'] == True:
                result.success(message)
            else:
                result.failure(message)

            return result

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            200: _handler_ok,
            401: handlers.auth_fail,
            405: handlers.method_not_allowed
        }


    def create_package(self, group_name, package_name, package_version, **kwargs):

        params = {
            'cmd': 'create',
            'groupName': group_name,
            'packageName': package_name,
            'packageVersion': package_version,
            '_charset_': 'utf-8'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/.json/etc/packages/{1}'.format(self.url, package_name)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def build_package(self, group_name, package_name, package_version, **kwargs):

        params = {
            'cmd': 'build'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(
            self.url, group_name, package_name, package_version)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def upload_package(self, group_name, package_name, package_version, file_path, **kwargs):

        file_name = '{0}-{1}.zip'.format(package_name, package_version)

        params = {
            'cmd': 'upload',
            'package': (pycurl.FORM_FILE, '{0}/{1}'.format(file_path.rstrip('/'), file_name))
        }

        opts = {
            'file_name': file_name
        }

        url = '{0}/crx/packmgr/service/.json/'.format(self.url)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = dict(self.kwargs.items() + opts.items())

        return bag.upload_file(url, params, _handlers, **opts)


    def install_package(self, group_name, package_name, package_version, **kwargs):

        # AEM might respond with '201 Created' after installing a package
        # this is actually a failure since the package status is uploaded but not installed
        def _handler_failure(response, **kwargs):

            data = json.loads(response['body'])
            message = 'AEM message: {0} - Installation failure, package status is uploaded but not installed'.format(
                data['msg'])
            result = res.PyAemResult(response)

            result.failure(message)

            return result

        params = {
            'cmd': 'install'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(
            self.url, group_name, package_name, package_version)
        params = dict(params.items() + kwargs.items())
        _handlers = {
            201: _handler_failure
        }

        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def replicate_package(self, group_name, package_name, package_version, **kwargs):

        params = {
            'cmd': 'replicate'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(
            self.url, group_name, package_name, package_version)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def delete_package(self, group_name, package_name, package_version, **kwargs):

        params = {
            'cmd': 'delete'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(
            self.url, group_name, package_name, package_version)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
