from mock import MagicMock
import pyaem
import unittest

class TestPyAem(unittest.TestCase):


  def test_init(self):

    aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
    self.assertTrue(hasattr(aem, 'content_repo'))
    self.assertTrue(hasattr(aem, 'package_manager'))
    self.assertTrue(hasattr(aem, 'web_console'))


  def test_init_ssl_debug(self):

    aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502, use_ssl = True, debug = True)
    self.assertTrue(hasattr(aem, 'content_repo'))
    self.assertTrue(hasattr(aem, 'package_manager'))
    self.assertTrue(hasattr(aem, 'web_console'))


  def test_create_path(self):

    aem = pyaem.PyAem('someusername', 'somepassword', 'localhost', 4502)
    aem.content_repo.create_path = MagicMock()
    
    aem.create_path('some/path')
    aem.content_repo.create_path.assert_called_once_with('some/path')


if __name__ == '__main__':
  unittest.main()