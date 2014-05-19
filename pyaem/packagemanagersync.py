from . import bagofrequests as bag
from BeautifulSoup import BeautifulSoup
from . import handlers
import json
import pycurl
from . import result as res

class PackageManagerSync(object):


    def __init__(self, url, **kwargs):

        def _handler_ok(response, **kwargs):

            soup = BeautifulSoup(response['body'],
                convertEntities=BeautifulSoup.HTML_ENTITIES
            )
            message_elem = soup.find('textarea')
            data = json.loads(message_elem.contents[0])
            message = data['msg']

            result = res.PyAemResult(response)
            if data['success'] == True:
                result.success(message)
            else:
                result.failure(message)
            return result

        def _handler_created(response, **kwargs):

            soup = BeautifulSoup(response['body'],
                convertEntities=BeautifulSoup.HTML_ENTITIES
            )
            message_elem = soup.find('div', {'id': 'Message'})
            message = message_elem.contents[0]

            result = res.PyAemResult(response)
            result.success(message)
            return result

        self.url = url
        self.kwargs = kwargs
        self.handlers = {
            200: _handler_ok,
            201: _handler_created,
            401: handlers.auth_fail
        }


    def upload_package(self, group_name, package_name, package_version, file_path, **kwargs):

        file_name = '{0}-{1}.zip'.format(package_name, package_version)

        params = {
            'cmd': 'upload',
            'package': (pycurl.FORM_FILE, '{0}/{1}'.format(file_path, file_name))
        }

        opts = {
            'file_name': file_name
        }

        url = '{0}/crx/packmgr/service/script.html/'.format(self.url)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = dict(self.kwargs.items() + opts.items())

        return bag.upload_file(url, params, _handlers, **opts)


    def install_package(self, group_name, package_name, package_version, **kwargs):

        params = {
            'cmd': 'install'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/script.html/etc/packages/{1}/{2}-{3}.zip'.format(
            self.url, group_name, package_name, package_version)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)


    def replicate_package(self, group_name, package_name, package_version, **kwargs):

        params = {
            'cmd': 'replicate'
        }

        method = 'post'
        url = '{0}/crx/packmgr/service/script.html/etc/packages/{1}/{2}-{3}.zip'.format(
            self.url, group_name, package_name, package_version)
        params = dict(params.items() + kwargs.items())
        _handlers = self.handlers
        opts = self.kwargs

        return bag.request(method, url, params, _handlers, **opts)
