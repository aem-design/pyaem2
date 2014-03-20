import crx

class PyAem(object):

	def __init__(self, username, password, host, port, use_ssl=False, debug=False):

		protocol = 'http' if use_ssl == False else 'https'
		url      = '{0}://{1}:{2}'.format(protocol, host, port)
		auth     = (username, password)
		self.crx = crx.Crx(url, auth, debug=debug)

	def create_package(self, group_name, package_name, package_version):

		self.crx.create_package(group_name, package_name, package_version)