import cStringIO
from .handlers import unexpected as handle_unexpected
import pycurl
import urllib

def request(method, url, params, handlers, **kwargs):
    """Sends HTTP request to a specified URL.
    Parameters will be appended to URL automatically on HTTP get method.
    Response code will then be used to determine which handler should process the response.
    When response code does not match any handler, an exception will be raised.

    :param method: HTTP method (post, delete, get)
    :type method: str
    :param url: URL to send HTTP request to
    :type url: str
    :param params: Request parameters key-value pairs, use array value to represent multi parameters with the same name
    :type params: dict
    :param handlers: Response handlers key-value pairs, keys are response http code, values are callback methods
    :type handlers: dict
    :returns:  PyAemResult -- Result of the request containing status, response http code and body, and request info
    :raises: PyAemException
    """
    curl = pycurl.Curl()
    body_io = cStringIO.StringIO()

    if method == 'post':
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(params, True))
    elif method == 'delete':
        curl.setopt(pycurl.CUSTOMREQUEST, method)
    elif method == 'head':
        curl.setopt(pycurl.HEADER, True)
        curl.setopt(pycurl.NOBODY, True)
    else:
        url = '{0}?{1}'.format(url, urllib.urlencode(params, True))

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.FRESH_CONNECT, 1)
    curl.setopt(pycurl.WRITEFUNCTION, body_io.write)

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': body_io.getvalue(),
        'request': {
            'method': method,
            'url': url,
            'params': params
        }
    }

    curl.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response, **kwargs)


def download_file(url, params, handlers, **kwargs):
    """Downloads a file from specified URL, the file will be downloaded to path specified in file kwarg.
    Parameters will be appended to URL automatically on HTTP get method.
    Response code will then be used to determine which handler should process the response.
    When response code does not match any handler, an exception will be raised.

    :param url: URL to send HTTP request to
    :type url: str
    :param params: Request parameters key-value pairs, use array value to represent multi parameters with the same name
    :type params: dict
    :param handlers: Response handlers key-value pairs, keys are response http code, values are callback methods
    :type handlers: dict
    :param kwargs: file (str) -- Location where the downloaded file will be saved to
    :type kwargs: dict
    :returns:  PyAemResult -- The result containing status, response http code and body, and request info
    :raises: PyAemException
    """
    curl = pycurl.Curl()
    url = '{0}?{1}'.format(url, urllib.urlencode(params, True))
    data = open(kwargs['file'], 'wb')

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.FRESH_CONNECT, 1)
    curl.setopt(pycurl.WRITEFUNCTION, data.write)

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': 'Download {0} to {1}'.format(url, kwargs['file']),
        'request': {
            'method': 'get',
            'url': url,
            'params': params
        }
    }

    curl.close()
    data.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response, **kwargs)


def upload_file(url, params, handlers, **kwargs):
    """Uploads a file using the specified URL endpoint,
    the file to be uploaded must be available at the specified location in file kwarg.
    Parameters will be appended to URL automatically on HTTP get method.
    Response code will then be used to determine which handler should process the response.
    When response code does not match any handler, an exception will be raised.

    :param url: URL to send HTTP request to
    :type url: str
    :param params: Request parameters key-value pairs, use array value to represent multi parameters with the same name
    :type params: dict
    :param handlers: Response handlers key-value pairs, keys are response http code, values are callback methods
    :type handlers: dict
    :param kwargs: file (str) -- Location of the file to be uploaded
    :type kwargs: dict
    :returns:  PyAemResult -- The result containing status, response http code and body, and request info
    :raises: PyAemException
    """
    curl = pycurl.Curl()
    body_io = cStringIO.StringIO()
    _params = []
    for key, value in params.iteritems():
        _params.append((key, value))

    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.HTTPPOST, _params)
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.FRESH_CONNECT, 1)
    curl.setopt(pycurl.WRITEFUNCTION, body_io.write)

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': body_io.getvalue(),
        'request': {
            'method': 'post',
            'url': url,
            'params': params
        }
    }

    curl.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response, **kwargs)
