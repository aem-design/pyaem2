import bagofrequests as bag
import handlers

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

	def create_package(self, group_name, package_name, package_version):

		url    = '{0}/crx/packmgr/service/.json/etc/packages/{1}?cmd=create'.format(self.url, package_name)
		params = {
			'groupName'     : group_name,
			'packageName'   : package_name,
			'packageVersion': package_version,
			'_charset_'     : 'utf-8'
		}

		bag.req('post', url, params, self.auth, self.handlers, debug=self.kwargs['debug'])