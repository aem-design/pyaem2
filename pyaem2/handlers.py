from bs4 import BeautifulSoup
from . import exception

def auth_fail(response, **kwargs):

    code = response['http_code']
    message = 'Authentication failed - incorrect username and/or password'

    raise exception.PyAem2Exception(code, message, response)


def method_not_allowed(response, **kwargs):

    code = response['http_code']
    soup = BeautifulSoup(response['body'], "html.parser")
    message = soup.title.string

    raise exception.PyAem2Exception(code, message, response)


def unexpected(response, **kwargs):

    code = response['http_code']
    message = 'Unexpected response\nhttp code: {0}\nbody:\n{1}'.format(response['http_code'], response['body'])

    raise exception.PyAem2Exception(code, message, response)
