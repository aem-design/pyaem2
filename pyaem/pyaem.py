import crx
import jcr

class PyAem(object):

	def __init__(self, username, password, host, port, use_ssl=False, debug=False):

		protocol = 'http' if use_ssl == False else 'https'
		url      = '{0}://{1}:{2}'.format(protocol, host, port)
		auth     = (username, password)
		self.crx = crx.Crx(url, auth, debug=debug)
		self.jcr = jcr.Jcr(url, auth, debug=debug)

	# crx methods

	def create_package(self, group_name, package_name, package_version, **kwargs):
		return self.crx.create_package(group_name, package_name, package_version, **kwargs)

	def update_package(self, group_name, package_name, package_version, **kwargs):
		return self.crx.update_package(group_name, package_name, package_version, **kwargs)

	def build_package(self, group_name, package_name, package_version, **kwargs):
	 	return self.crx.build_package(group_name, package_name, package_version, **kwargs)

	def download_package(self, group_name, package_name, package_version, **kwargs):
		return self.crx.download_package(group_name, package_name, package_version, **kwargs)

	def upload_package(self, group_name, package_name, package_version, **kwargs):
		return self.crx.upload_package(group_name, package_name, package_version, **kwargs)

	def install_package(self, group_name, package_name, package_version, **kwargs):
		return self.crx.install_package(group_name, package_name, package_version, **kwargs)

	# jcr methods

	def activate_tree(self, path, **kwargs):
		return self.jcr.activate_tree(path, **kwargs)