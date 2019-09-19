import unittest
from six import BytesIO
from mock import MagicMock
import mock
import pyaem2
from pyaem2 import result as res
import pycurl

class TestBagOfRequests(unittest.TestCase):
    def _handler_dummy(self, response, **kwargs):

        result = res.PyAem2Result(response)
        result.success('some dummy message')
        return result

    def test_import_bytesio(self):
        body_io = BytesIO(b"abcdef")
        self.assertEqual(body_io.getvalue().decode('utf-8'), "abcdef")

    def test_request_post(self):

        curl = pycurl.Curl()
        curl.setopt = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value=200)
        curl.close = MagicMock()
        pycurl.Curl = MagicMock(return_value=curl)

        method = 'post'
        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': ['bar2a', 'bar2b']}
        handlers = {200: self._handler_dummy}

        result = pyaem2.bagofrequests.request(method, url, params, handlers)

        curl.setopt.assert_any_call(pycurl.POST, 1)
        curl.setopt.assert_any_call(pycurl.POSTFIELDS, 'foo1=bar1&foo2=bar2a&foo2=bar2b')
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 6 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 6)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result.is_success(), True)
        self.assertEqual(result.message, 'some dummy message')
        self.assertEqual(result.response['request']['method'], 'post')
        self.assertEqual(result.response['request']['url'], 'http://localhost:4502/.cqactions.html')
        self.assertEqual(result.response['request']['params'], params)

    def test_request_get(self):

        curl = pycurl.Curl()
        curl.setopt = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value=200)
        curl.close = MagicMock()
        pycurl.Curl = MagicMock(return_value=curl)

        method = 'get'
        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': ['bar2a', 'bar2b']}
        handlers = {200: self._handler_dummy}

        result = pyaem2.bagofrequests.request(method, url, params, handlers)

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2a&foo2=bar2b')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 4 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 4)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result.is_success(), True)
        self.assertEqual(result.message, 'some dummy message')
        self.assertEqual(result.response['request']['method'], 'get')
        self.assertEqual(result.response['request']['url'],
                         'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2a&foo2=bar2b')
        self.assertEqual(result.response['request']['params'], params)

    def test_request_delete(self):

        curl = pycurl.Curl()
        curl.setopt = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value=200)
        curl.close = MagicMock()
        pycurl.Curl = MagicMock(return_value=curl)

        method = 'delete'
        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': ['bar2a', 'bar2b']}
        handlers = {200: self._handler_dummy}

        result = pyaem2.bagofrequests.request(method, url, params, handlers)

        curl.setopt.assert_any_call(pycurl.CUSTOMREQUEST, 'delete')
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 5 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 5)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result.is_success(), True)
        self.assertEqual(result.message, 'some dummy message')
        self.assertEqual(result.response['request']['method'], 'delete')
        self.assertEqual(result.response['request']['url'], 'http://localhost:4502/.cqactions.html')
        self.assertEqual(result.response['request']['params'], params)

    def test_request_head(self):

        curl = pycurl.Curl()
        curl.setopt = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value=200)
        curl.close = MagicMock()
        pycurl.Curl = MagicMock(return_value=curl)

        method = 'head'
        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': ['bar2a', 'bar2b']}
        handlers = {200: self._handler_dummy}

        result = pyaem2.bagofrequests.request(method, url, params, handlers)

        curl.setopt.assert_any_call(pycurl.HEADER, True)
        curl.setopt.assert_any_call(pycurl.NOBODY, True)
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 6 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 6)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result.is_success(), True)
        self.assertEqual(result.message, 'some dummy message')
        self.assertEqual(result.response['request']['method'], 'head')
        self.assertEqual(result.response['request']['url'], 'http://localhost:4502/.cqactions.html')
        self.assertEqual(result.response['request']['params'], params)

    def test_request_unexpected_resp(self):

        method = 'get'
        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': 'bar2'}
        handlers = {200: self._handler_dummy}
        response_content = 'Unexpected response\nhttp code: 500\nbody:\n'

        response = {
            'http_code': 500,
            'body': response_content,
            'method': method,
            'request': {
                'method': 'post',
                'url': url,
                'params': params
            }
        }

        curl = mock.MagicMock()
        curl.getinfo = mock.Mock(return_value=500)
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.close = mock.Mock()
        pycurl.Curl = mock.MagicMock(return_value=curl)

        mock_io_string = mock.MagicMock()
        mock_io_string.getvalue = mock.Mock(return_value=response_content)

        try:
            with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                with mock.patch('io.BytesIO', mock.Mock(return_value=mock_io_string)):
                    result = pyaem2.bagofrequests.request(method, url, params, handlers)
                    self.assertEqual(result, response)
            # pyaem2.bagofrequests.request(method, url, params, handlers)
            self.fail('An exception should have been raised')
        except pyaem2.PyAem2Exception as exception:
            self.assertEqual(exception.code, 500)
            self.assertEqual(exception.message, 'Unexpected response\nhttp code: 500\nbody:\n')

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 4 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 4)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

    def test_download_file(self):

        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': ['bar2a', 'bar2b']}
        handlers = {200: self._handler_dummy}

        curl = mock.MagicMock()
        curl.getinfo = mock.Mock(return_value=200)
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.close = mock.Mock()
        pycurl.Curl = mock.MagicMock(return_value=curl)

        with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
            result = pyaem2.bagofrequests.download_file(url, params, handlers, file='/tmp/somefile')

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2a&foo2=bar2b')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 4 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 4)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result.is_success(), True)
        self.assertEqual(result.message, 'some dummy message')
        self.assertEqual(result.response['request']['method'], 'get')
        self.assertEqual(result.response['request']['url'],
                         'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2a&foo2=bar2b')
        self.assertEqual(result.response['request']['params'], params)

    def test_download_file_unexpected(self):

        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': 'bar2'}
        handlers = {}
        response_content = 'Download http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2 to /tmp/somefile'

        response = {
            'http_code': 500,
            'body': response_content,
            'request': {
                'method': 'get',
                'url': url,
                'params': params
            }
        }

        curl = mock.MagicMock()
        curl.getinfo = mock.Mock(return_value=500)
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.close = mock.Mock()
        pycurl.Curl = mock.MagicMock(return_value=curl)

        mock_io_string = mock.MagicMock()
        mock_io_string.getvalue = mock.Mock(return_value=response_content)

        try:
            with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                with mock.patch('io.BytesIO', mock.Mock(return_value=mock_io_string)):
                    self.assertEqual(pyaem2.bagofrequests.download_file(url, params, handlers, file='/tmp/somefile'), (response, '/tmp/somefile'))
            self.fail('An exception should have been raised')
        except pyaem2.PyAem2Exception as exception:
            self.assertEqual(exception.code, 500)
            self.assertEqual(exception.message,
                             'Unexpected response\nhttp code: 500\nbody:\n' +
                             'Download http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2 to /tmp/somefile')

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 5 calls including the one with pycurl.WRITEDATA and pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 4)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

    def test_upload_file(self):

        curl = mock.MagicMock()
        curl.getinfo = mock.Mock(return_value=200)
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.close = mock.Mock()
        pycurl.Curl = mock.MagicMock(return_value=curl)

        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': 'bar2'}
        handlers = {200: self._handler_dummy}

        with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
            result = pyaem2.bagofrequests.upload_file(url, params, handlers, file='/tmp/somefile')

        curl.setopt.assert_any_call(pycurl.POST, 1)
        curl.setopt.assert_any_call(pycurl.HTTPPOST, [('foo1', 'bar1'), ('foo2', 'bar2')])
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 6 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 6)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result.is_success(), True)
        self.assertEqual(result.message, 'some dummy message')
        self.assertEqual(result.response['request']['method'], 'post')
        self.assertEqual(result.response['request']['url'], 'http://localhost:4502/.cqactions.html')
        self.assertEqual(result.response['request']['params'], params)

    def test_upload_file_unexpected(self):

        url = 'http://localhost:4502/.cqactions.html'
        params = {'foo1': 'bar1', 'foo2': 'bar2'}
        handlers = {}
        response_content = 'Unexpected response\nhttp code: 500\nbody:\n'

        response = {
            'http_code': 500,
            'body': response_content,
            'request': {
                'method': 'post',
                'url': url,
                'params': params
            }
        }

        curl = mock.MagicMock()
        curl.getinfo = mock.Mock(return_value=500)
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.close = mock.Mock()
        pycurl.Curl = mock.MagicMock(return_value=curl)

        mock_io_string = mock.MagicMock()
        mock_io_string.getvalue = mock.Mock(return_value=response_content)

        try:
            with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                with mock.patch('io.BytesIO', mock.Mock(return_value=mock_io_string)):
                    self.assertEqual(pyaem2.bagofrequests.upload_file(url, params, handlers, file='/tmp/somefile'), (response, '/tmp/somefile'))
                self.fail('An exception should have been raised')
        except pyaem2.PyAem2Exception as exception:
            self.assertEqual(exception.code, 500)
            self.assertEqual(exception.message, 'Unexpected response\nhttp code: 500\nbody:\n')

        curl.setopt.assert_any_call(pycurl.POST, 1)
        curl.setopt.assert_any_call(pycurl.HTTPPOST, [('foo1', 'bar1'), ('foo2', 'bar2')])
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)
        curl.setopt.assert_any_call(pycurl.FRESH_CONNECT, 1)

        # 6 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 6)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
