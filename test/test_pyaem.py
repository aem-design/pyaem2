from mock import MagicMock
import pyaem
import unittest

class TestPyAem(unittest.TestCase):


    def setUp(self):

        self.aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)


    def test_init(self):

        self.assertTrue(hasattr(self.aem, 'content_repo'))
        self.assertTrue(hasattr(self.aem, 'package_manager'))
        self.assertTrue(hasattr(self.aem, 'package_manager_service_html'))
        self.assertTrue(hasattr(self.aem, 'package_manager_service_json'))
        self.assertTrue(hasattr(self.aem, 'package_manager_service_jsp'))
        self.assertTrue(hasattr(self.aem, 'web_console'))


    def test_init_ssl_debug(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502, use_ssl=True, debug=True)
        self.assertTrue(hasattr(aem, 'content_repo'))
        self.assertTrue(hasattr(aem, 'package_manager'))
        self.assertTrue(hasattr(aem, 'package_manager_service_html'))
        self.assertTrue(hasattr(aem, 'package_manager_service_json'))
        self.assertTrue(hasattr(aem, 'package_manager_service_jsp'))
        self.assertTrue(hasattr(aem, 'web_console'))


    # content repo methods


    def test_create_path(self):

        self.aem.content_repo.create_path = MagicMock()

        self.aem.create_path('/content/somepath')
        self.aem.content_repo.create_path.assert_called_once_with('/content/somepath')


    def test_delete_path(self):

        self.aem.content_repo.delete_path = MagicMock()

        self.aem.delete_path('/content/somepath')
        self.aem.content_repo.delete_path.assert_called_once_with('/content/somepath')


    def test_activate_path(self):

        self.aem.content_repo.activate_path = MagicMock()

        self.aem.activate_path('/content/somepath')
        self.aem.content_repo.activate_path.assert_called_once_with('/content/somepath')


    def test_does_user_exist(self):

        self.aem.content_repo.does_user_exist = MagicMock()

        self.aem.does_user_exist('/home/users/u/', 'someusername1')
        self.aem.content_repo.does_user_exist.assert_called_once_with('/home/users/u/', 'someusername1')


    def test_create_user(self):

        self.aem.content_repo.create_user = MagicMock()

        self.aem.create_user('/home/users/u/', 'someusername1', 'somepassword1')
        self.aem.content_repo.create_user.assert_called_once_with('/home/users/u/', 'someusername1', 'somepassword1')


    def test_add_user_to_group(self):

        self.aem.content_repo.add_user_to_group = MagicMock()

        self.aem.add_user_to_group('someusername1', '/home/groups/g/', 'somegroupname1')
        self.aem.content_repo.add_user_to_group.assert_called_once_with(
            'someusername1', '/home/groups/g/', 'somegroupname1')


    def test_does_group_exist(self):

        self.aem.content_repo.does_group_exist = MagicMock()

        self.aem.does_group_exist('/home/groups/g/', 'somegroupname1')
        self.aem.content_repo.does_group_exist.assert_called_once_with('/home/groups/g/', 'somegroupname1')


    def test_create_group(self):

        self.aem.content_repo.create_group = MagicMock()

        self.aem.create_group('/home/groups/g/', 'somegroupname1')
        self.aem.content_repo.create_group.assert_called_once_with('/home/groups/g/', 'somegroupname1')


    def test_change_password(self):

        self.aem.content_repo.change_password = MagicMock()

        self.aem.change_password('/home/users/u/', 'someusername1', 'someoldpassword', 'somenewpassword')
        self.aem.content_repo.change_password.assert_called_once_with(
            '/home/users/u/', 'someusername1', 'someoldpassword', 'somenewpassword')


    def test_set_permission(self):

        self.aem.content_repo.set_permission = MagicMock()

        self.aem.set_permission('somegroup', '/content/somesite', 'read:true,modify:true')
        self.aem.content_repo.set_permission.assert_called_once_with(
            'somegroup', '/content/somesite', 'read:true,modify:true')


    def test_create_agent(self):

        self.aem.content_repo.create_agent = MagicMock()

        self.aem.create_agent(
            'someagent', 'flush', 'someuser', 'somepassword', 'http://somehost:8080', 'publish')
        self.aem.content_repo.create_agent.assert_called_once_with(
            'someagent', 'flush', 'someuser', 'somepassword', 'http://somehost:8080', 'publish')


    def test_delete_agent(self):

        self.aem.content_repo.delete_agent = MagicMock()

        self.aem.delete_agent('someagentname', 'somerunmode')
        self.aem.content_repo.delete_agent.assert_called_once_with('someagentname', 'somerunmode')


    def test_set_property(self):

        self.aem.content_repo.set_property = MagicMock()

        self.aem.set_property('/content/mysite', 'sling:target', '/welcome.html')
        self.aem.content_repo.set_property.assert_called_once_with('/content/mysite', 'sling:target', '/welcome.html')


    def test_enable_workflow(self):

        self.aem.content_repo.enable_workflow = MagicMock()

        self.aem.enable_workflow(
            '/etc/workflow/models/dam/update_asset/jcr:content/model',
            '/content/dam(/.*/)renditions/original',
            '/etc/workflow/launcher/config/update_asset_mod',
            'nt:file',
            'author')
        self.aem.content_repo.enable_workflow.assert_called_once_with(
            '/etc/workflow/models/dam/update_asset/jcr:content/model',
            '/content/dam(/.*/)renditions/original',
            '/etc/workflow/launcher/config/update_asset_mod',
            'nt:file',
            'author')


    def test_disable_workflow(self):

        self.aem.content_repo.disable_workflow = MagicMock()

        self.aem.disable_workflow(
            '/etc/workflow/models/dam/update_asset/jcr:content/model',
            '/content/dam(/.*/)renditions/original',
            '/etc/workflow/launcher/config/update_asset_mod',
            'nt:file',
            'author')
        self.aem.content_repo.disable_workflow.assert_called_once_with(
            '/etc/workflow/models/dam/update_asset/jcr:content/model',
            '/content/dam(/.*/)renditions/original',
            '/etc/workflow/launcher/config/update_asset_mod',
            'nt:file',
            'author')


    def test_get_cluster_list(self):

        self.aem.content_repo.get_cluster_list = MagicMock()

        self.aem.get_cluster_list()
        self.aem.content_repo.get_cluster_list.assert_called_once_with()


    # package manager methods


    def test_update_package(self):

        self.aem.package_manager.update_package = MagicMock()

        self.aem.update_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager.update_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_download_package(self):

        self.aem.package_manager.download_package = MagicMock()

        self.aem.download_package('somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')
        self.aem.package_manager.download_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')


    # package manager service/.json methods


    def test_create_package(self):

        self.aem.package_manager_service_json.create_package = MagicMock()

        self.aem.create_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_json.create_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_build_package(self):

        self.aem.package_manager_service_json.build_package = MagicMock()

        self.aem.build_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_json.build_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_upload_package(self):

        self.aem.package_manager_service_json.upload_package = MagicMock()

        self.aem.upload_package('somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')
        self.aem.package_manager_service_json.upload_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')


    def test_install_package(self):

        self.aem.package_manager_service_json.install_package = MagicMock()

        self.aem.install_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_json.install_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_replicate_package(self):

        self.aem.package_manager_service_json.replicate_package = MagicMock()

        self.aem.replicate_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_json.replicate_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_delete_package(self):

        self.aem.package_manager_service_json.delete_package = MagicMock()

        self.aem.delete_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_json.delete_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    # package manager service.jsp methods


    def test_is_package_uploaded(self):

        self.aem.package_manager_service_jsp.is_package_uploaded = MagicMock()

        self.aem.is_package_uploaded('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_jsp.is_package_uploaded.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_is_package_installed(self):

        self.aem.package_manager_service_jsp.is_package_installed = MagicMock()

        self.aem.is_package_installed('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_jsp.is_package_installed.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    # package manager service/script.html methods


    def test_upload_pkg_service_html(self):

        self.aem.package_manager_service_html.upload_package = MagicMock()

        self.aem.upload_package_sync('somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')
        self.aem.package_manager_service_html.upload_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')


    def test_install_pkg_service_html(self):

        self.aem.package_manager_service_html.install_package = MagicMock()

        self.aem.install_package_sync('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_html.install_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_replicate_pkg_service_html(self):

        self.aem.package_manager_service_html.replicate_package = MagicMock()

        self.aem.replicate_package_sync('somegroup', 'somepackage', '1.2-SNAPSHOT')
        self.aem.package_manager_service_html.replicate_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT')


    # web console methods


    def test_start_bundle(self):

        self.aem.web_console.start_bundle = MagicMock()

        self.aem.start_bundle('somebundle')
        self.aem.web_console.start_bundle.assert_called_once_with('somebundle')


    def test_stop_bundle(self):

        self.aem.web_console.stop_bundle = MagicMock()

        self.aem.stop_bundle('somebundle')
        self.aem.web_console.stop_bundle.assert_called_once_with('somebundle')


    def test_install_bundle(self):

        self.aem.web_console.install_bundle = MagicMock()

        self.aem.install_bundle('somebundle', '1.2-SNAPSHOT', '/mnt/ephemeral0')
        self.aem.web_console.install_bundle.assert_called_once_with('somebundle', '1.2-SNAPSHOT', '/mnt/ephemeral0')


    # sling methods


    def test_is_valid_login(self):

        self.aem.sling.is_valid_login = MagicMock()

        self.aem.is_valid_login()
        self.aem.sling.is_valid_login.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
    