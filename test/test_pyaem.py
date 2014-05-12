from mock import MagicMock
import pyaem
import unittest

class TestPyAem(unittest.TestCase):


    def test_init(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        self.assertTrue(hasattr(aem, 'content_repo'))
        self.assertTrue(hasattr(aem, 'package_manager'))
        self.assertTrue(hasattr(aem, 'package_manager_sync'))
        self.assertTrue(hasattr(aem, 'web_console'))


    def test_init_ssl_debug(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502, use_ssl=True, debug=True)
        self.assertTrue(hasattr(aem, 'content_repo'))
        self.assertTrue(hasattr(aem, 'package_manager'))
        self.assertTrue(hasattr(aem, 'package_manager_sync'))
        self.assertTrue(hasattr(aem, 'web_console'))


    # content repo methods


    def test_create_path(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.create_path = MagicMock()

        aem.create_path('/content/somepath')
        aem.content_repo.create_path.assert_called_once_with('/content/somepath')


    def test_activate_path(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.activate_path = MagicMock()

        aem.activate_path('/content/somepath')
        aem.content_repo.activate_path.assert_called_once_with('/content/somepath')


    def test_create_user(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.create_user = MagicMock()

        aem.create_user('/home/users/u/', 'someusername1', 'somepassword1')
        aem.content_repo.create_user.assert_called_once_with('/home/users/u/', 'someusername1', 'somepassword1')


    def test_add_user_to_group(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.add_user_to_group = MagicMock()

        aem.add_user_to_group('someusername1', '/home/groups/g/', 'somegroupname1')
        aem.content_repo.add_user_to_group.assert_called_once_with('someusername1', '/home/groups/g/', 'somegroupname1')


    def test_create_group(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.create_group = MagicMock()

        aem.create_group('/home/groups/g/', 'somegroupname1')
        aem.content_repo.create_group.assert_called_once_with('/home/groups/g/', 'somegroupname1')


    def test_change_password(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.change_password = MagicMock()

        aem.change_password('/home/users/u/', 'someusername1', 'someoldpassword', 'somenewpassword')
        aem.content_repo.change_password.assert_called_once_with(
            '/home/users/u/', 'someusername1', 'someoldpassword', 'somenewpassword')


    def test_set_permission(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.set_permission = MagicMock()

        aem.set_permission('somegroup', '/content/somesite', 'read:true,modify:true')
        aem.content_repo.set_permission.assert_called_once_with(
            'somegroup', '/content/somesite', 'read:true,modify:true')


    def test_create_agent(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.create_agent = MagicMock()

        aem.create_agent(
            'someagent', 'flush', 'someuser', 'somepassword', 'http://somehost:8080', 'publish')
        aem.content_repo.create_agent.assert_called_once_with(
            'someagent', 'flush', 'someuser', 'somepassword', 'http://somehost:8080', 'publish')


    def test_delete_agent(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.content_repo.delete_agent = MagicMock()

        aem.delete_agent('someagentname', 'somerunmode')
        aem.content_repo.delete_agent.assert_called_once_with('someagentname', 'somerunmode')


    # package manager methods


    def test_create_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.create_package = MagicMock()

        aem.create_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager.create_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_update_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.update_package = MagicMock()

        aem.update_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager.update_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_build_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.build_package = MagicMock()

        aem.build_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager.build_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_download_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.download_package = MagicMock()

        aem.download_package('somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')
        aem.package_manager.download_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')


    def test_upload_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.upload_package = MagicMock()

        aem.upload_package('somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')
        aem.package_manager.upload_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')


    def test_install_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.install_package = MagicMock()

        aem.install_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager.install_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_replicate_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.replicate_package = MagicMock()

        aem.replicate_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager.replicate_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_delete_package(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager.delete_package = MagicMock()

        aem.delete_package('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager.delete_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    # package manager methods


    def test_upload_package_sync(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager_sync.upload_package = MagicMock()

        aem.upload_package_sync('somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')
        aem.package_manager_sync.upload_package.assert_called_once_with(
            'somegroup', 'somepackage', '1.2-SNAPSHOT', '/some/path/')


    def test_install_package_sync(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager_sync.install_package = MagicMock()

        aem.install_package_sync('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager_sync.install_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    def test_replicate_package_sync(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.package_manager_sync.replicate_package = MagicMock()

        aem.replicate_package_sync('somegroup', 'somepackage', '1.2-SNAPSHOT')
        aem.package_manager_sync.replicate_package.assert_called_once_with('somegroup', 'somepackage', '1.2-SNAPSHOT')


    # web console methods


    def test_start_bundle(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.web_console.start_bundle = MagicMock()

        aem.start_bundle('somebundle')
        aem.web_console.start_bundle.assert_called_once_with('somebundle')


    def test_stop_bundle(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.web_console.stop_bundle = MagicMock()

        aem.stop_bundle('somebundle')
        aem.web_console.stop_bundle.assert_called_once_with('somebundle')


    def test_install_bundle(self):

        aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
        aem.web_console.install_bundle = MagicMock()

        aem.install_bundle('somebundle', '1.2-SNAPSHOT', '/mnt/ephemeral0')
        aem.web_console.install_bundle.assert_called_once_with('somebundle', '1.2-SNAPSHOT', '/mnt/ephemeral0')


if __name__ == '__main__':
    unittest.main()
    