from . import bagofrequests as bag
from . import handlers
from . import result as res
import xmltodict

class PackageManagerServiceJsp(object):


    def __init__(self, url, **kwargs):

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            401: handlers.auth_fail
        }


    def is_package_uploaded(self, group_name, package_name, package_version, **kwargs):

        def _handler_ok(response, **kwargs):

            data = xmltodict.parse(response['body'])
            status_code = data['crx']['response']['status']['@code']
            status_value = data['crx']['response']['status']['#text']
            result = res.PyAemResult(response)

            if status_code != '200' or status_value != 'ok':

                message = 'Unable to retrieve package list. Command status code {0} and status value {1}'.format(
                    status_code, status_value)
                result.failure(message)

            else:

                def match(package):
                    # when version value is not specified, the version xml element will be empty <version></version>
                    if package['version'] == None:
                        package['version'] = ''
                    return (package['group'] == group_name and
                        package['name'] == package_name and
                        package['version'] == package_version)

                is_uploaded = False
                packages = data['crx']['response']['data']['packages']
                if packages != None:
                    if isinstance(packages['package'], list):
                        for package in packages['package']:
                            if match(package):
                                is_uploaded = True
                    elif match(packages['package']):
                        is_uploaded = True

                if is_uploaded == True:
                    message = 'Package {0}/{1}-{2} is uploaded'.format(group_name, package_name, package_version)
                    result.success(message)
                else:
                    message = 'Package {0}/{1}-{2} is not uploaded'.format(group_name, package_name, package_version)
                    result.failure(message)

            return result

        _handlers = {
            200: _handler_ok
        }

        params = {
            'cmd': 'ls'
        }

        method = 'get'
        url = '{0}/crx/packmgr/service.jsp'.format(self.url, package_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def is_package_installed(self, group_name, package_name, package_version, **kwargs):

        def _handler_ok(response, **kwargs):

            data = xmltodict.parse(response['body'])
            status_code = data['crx']['response']['status']['@code']
            status_value = data['crx']['response']['status']['#text']
            result = res.PyAemResult(response)

            if status_code != '200' or status_value != 'ok':

                message = 'Unable to retrieve package list. Command status code {0} and status value {1}'.format(
                    status_code, status_value)
                result.failure(message)

            else:

                def match(package):
                    # when version value is not specified, the version xml element will be empty <version></version>
                    if package['version'] == None:
                        package['version'] = ''
                    return (package['group'] == group_name and
                        package['name'] == package_name and
                        package['version'] == package_version and
                        package['lastUnpackedBy'] != 'null')

                is_installed = False
                packages = data['crx']['response']['data']['packages']
                if packages != None:
                    if isinstance(packages['package'], list):
                        for package in packages['package']:
                            if match(package):
                                is_installed = True
                    elif match(packages['package']):
                        is_installed = True

                if is_installed == True:
                    message = 'Package {0}/{1}-{2} is installed'.format(group_name, package_name, package_version)
                    result.success(message)
                else:
                    message = 'Package {0}/{1}-{2} is not installed'.format(group_name, package_name, package_version)
                    result.failure(message)

            return result

        _handlers = {
            200: _handler_ok
        }

        params = {
            'cmd': 'ls'
        }

        method = 'get'
        url = '{0}/crx/packmgr/service.jsp'.format(self.url, package_name)
        params = dict(params.items() + kwargs.items())
        _handlers = dict(self.handlers.items() + _handlers.items())
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
