import pyaem
import unittest

class TestException(unittest.TestCase):


    def test_init(self):

        response = {'body': 'some body'}
        exception = pyaem.PyAemException(123, 'somemessage', response)
        self.assertEqual(exception.code, 123)
        self.assertEqual(exception.message, 'somemessage')
        self.assertEqual(exception.response['body'], 'some body')


if __name__ == '__main__':
    unittest.main()
    