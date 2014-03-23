import packagemanager
import jcr

class PyAem(object):


	def __init__(self, username, password, host, port, use_ssl=False, debug=False):

		protocol = 'http' if use_ssl == False else 'https'
		url      = '{0}://{1}:{2}@{3}:{4}'.format(protocol, username, password, host, port)

		self.package_manager = packagemanager.PackageManager(url, debug=debug)
		self.jcr = jcr.Jcr(url, debug=debug)


	# crx package manager methods


	def create_package(self, group_name, package_name, package_version, **kwargs):
		return self.package_manager.create_package(group_name, package_name, package_version, **kwargs)


	def update_package(self, group_name, package_name, package_version, **kwargs):
		return self.package_manager.update_package(group_name, package_name, package_version, **kwargs)


	def build_package(self, group_name, package_name, package_version, **kwargs):
	 	return self.package_manager.build_package(group_name, package_name, package_version, **kwargs)


	def download_package(self, group_name, package_name, package_version, **kwargs):
		return self.package_manager.download_package(group_name, package_name, package_version, **kwargs)


	def upload_package(self, group_name, package_name, package_version, **kwargs):
		return self.package_manager.upload_package(group_name, package_name, package_version, **kwargs)


	def install_package(self, group_name, package_name, package_version, **kwargs):
		return self.package_manager.install_package(group_name, package_name, package_version, **kwargs)


	# jcr methods


	def activate_tree(self, path, **kwargs):
		return self.jcr.activate_tree(path, **kwargs)