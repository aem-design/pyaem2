import bagofrequests as bag
import handlers
import json

class Crx(object):

	def __init__(self, url, auth, **kwargs):

		self.url    = url
		self.auth   = auth
		self.kwargs = kwargs

		self.handlers = {
			200: handlers.ok_json,
			401: handlers.auth_fail,
			403: handlers.auth_required,
			405: handlers.method_not_allowed
		}

	def create_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'groupName'     : group_name,
			'packageName'   : package_name,
			'packageVersion': package_version,
			'_charset_'     : 'utf-8'
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}?cmd=create'.format(self.url, package_name)
		params   = dict(params.items() + kwargs.items())
		auth     = self.auth
		handlers = self.handlers
		opts     = self.kwargs

		return bag.req(method, url, params, auth, handlers, **opts)

	def update_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'groupName'  : group_name,
			'packageName': package_name,
			'version'    : package_version,
			'path'       : '/etc/packages/{0}/{1}-{2}.zip'.format(group_name, package_name, package_version),
			'_charset_'  : 'utf-8'
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/update.jsp'.format(self.url)
		params   = dict(params.items() + kwargs.items())
		auth     = self.auth
		handlers = self.handlers
		opts     = self.kwargs

		return bag.req(method, url, params, auth, handlers, **opts)

	def build_package(self, group_name, package_name, package_version, **kwargs):

		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip?cmd=build'.format(self.url, group_name, package_name, package_version)
		params   = kwargs
		auth     = self.auth
		handlers = self.handlers
		opts     = self.kwargs

		return bag.req(method, url, params, auth, handlers, **opts)

	def download_package(self, group_name, package_name, package_version, **kwargs):

		_handlers = {
			200: handlers.ok_file
		}
		opts      = {
			'stream': True,
			'file'  : '{0}-{1}.zip'.format(package_name, package_version)
		}
		method    = 'get'
		url       = '{0}/etc/packages/{1}/{2}-{3}.zip'.format(self.url, group_name, package_name, package_version)
		params    = kwargs
		auth      = self.auth
		_handlers = dict(self.handlers.items() + _handlers.items())
		opts      = dict(self.kwargs.items() + opts.items())

		return bag.req(method, url, params, auth, _handlers, **opts)

	def upload_package(self, group_name, package_name, package_version, **kwargs):

		opts     = {
			'files': {
				'package': open('{0}-{1}.zip'.format(package_name, package_version), 'rb')
			}
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/?cmd=upload'.format(self.url)
		params   = kwargs
		auth     = self.auth
		handlers = self.handlers
		opts     = dict(self.kwargs.items() + opts.items())

		return bag.req(method, url, params, auth, handlers, **opts)

	def install_package(self, group_name, package_name, package_version, **kwargs):

		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip?cmd=install'.format(self.url, group_name, package_name, package_version)
		params   = kwargs
		auth     = self.auth
		handlers = self.handlers
		opts     = self.kwargs

		return bag.req(method, url, params, auth, handlers, **opts)