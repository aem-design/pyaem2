from . import contentrepo
from . import packagemanager
from . import packagemanagersync
from . import webconsole

class PyAem(object):


    def __init__(self, username, password, host, port, use_ssl=False, debug=False):

        protocol = 'http' if use_ssl == False else 'https'
        url = '{0}://{1}:{2}@{3}:{4}'.format(protocol, username, password, host, port)

        self.content_repo = contentrepo.ContentRepo(url, debug=debug)
        self.package_manager = packagemanager.PackageManager(url, debug=debug)
        self.package_manager_sync = packagemanagersync.PackageManagerSync(url, debug=debug)
        self.web_console = webconsole.WebConsole(url, debug=debug)


    # content repo methods


    def create_path(self, path, **kwargs):
        return self.content_repo.create_path(path, **kwargs)


    def activate_path(self, path, **kwargs):
        return self.content_repo.activate_path(path, **kwargs)


    def create_user(self, user_path, user_name, password, **kwargs):
        return self.content_repo.create_user(user_path, user_name, password, **kwargs)


    def add_user_to_group(self, user_name, group_path, group_name, **kwargs):
        return self.content_repo.add_user_to_group(user_name, group_path, group_name, **kwargs)


    def create_group(self, group_path, group_name, **kwargs):
        return self.content_repo.create_group(group_path, group_name, **kwargs)


    def change_password(self, user_path, user_name, old_password, new_password, **kwargs):
        return self.content_repo.change_password(user_path, user_name, old_password, new_password, **kwargs)


    def set_permission(self, user_or_group_name, path, permissions, **kwargs):
        return self.content_repo.set_permission(user_or_group_name, path, permissions, **kwargs)


    def create_agent(self, agent_name, agent_type, dest_username, dest_password, dest_url, run_mode, **kwargs):
        return self.content_repo.create_agent(
            agent_name, agent_type, dest_username, dest_password, dest_url, run_mode, **kwargs)


    def delete_agent(self, agent_name, run_mode, **kwargs):
        return self.content_repo.delete_agent(agent_name, run_mode, **kwargs)


    # package manager methods


    def create_package(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager.create_package(group_name, package_name, package_version, **kwargs)


    def update_package(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager.update_package(group_name, package_name, package_version, **kwargs)


    def build_package(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager.build_package(group_name, package_name, package_version, **kwargs)


    def download_package(self, group_name, package_name, package_version, file_path, **kwargs):
        return self.package_manager.download_package(group_name, package_name, package_version, file_path, **kwargs)


    def upload_package(self, group_name, package_name, package_version, file_path, **kwargs):
        return self.package_manager.upload_package(group_name, package_name, package_version, file_path, **kwargs)


    def install_package(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager.install_package(group_name, package_name, package_version, **kwargs)


    def replicate_package(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager.replicate_package(group_name, package_name, package_version, **kwargs)


    def delete_package(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager.delete_package(group_name, package_name, package_version, **kwargs)


    # synchronous package manager methods


    def upload_package_sync(self, group_name, package_name, package_version, file_path, **kwargs):
        return self.package_manager_sync.upload_package(group_name, package_name, package_version, file_path, **kwargs)


    def install_package_sync(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager_sync.install_package(group_name, package_name, package_version, **kwargs)


    def replicate_package_sync(self, group_name, package_name, package_version, **kwargs):
        return self.package_manager_sync.replicate_package(group_name, package_name, package_version, **kwargs)


    # web console methods


    def start_bundle(self, bundle_name, **kwargs):
        return self.web_console.start_bundle(bundle_name, **kwargs)


    def stop_bundle(self, bundle_name, **kwargs):
        return self.web_console.stop_bundle(bundle_name, **kwargs)


    def install_bundle(self, bundle_name, bundle_version, file_path, **kwargs):
        return self.web_console.install_bundle(bundle_name, bundle_version, file_path, **kwargs)
