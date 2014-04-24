import pyaem
import unittest

class TestContentRepo(unittest.TestCase):


    def test_init(self):

        contentrepo = pyaem.contentrepo.ContentRepo('http://localhost:4502/.cqactions.html', foo='bar')

        self.assertEqual(contentrepo.url, 'http://localhost:4502/.cqactions.html')
        self.assertEqual(contentrepo.kwargs['foo'], 'bar')

        self.assertTrue(401 in contentrepo.handlers)
        self.assertTrue(405 in contentrepo.handlers)

if __name__ == '__main__':
    unittest.main()
    