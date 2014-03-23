from BeautifulSoup import *
import exception

def auth_fail(response, **kwargs):

	code    = response['http_code']
	message = 'Authentication failed - incorrect username and/or password'

	raise exception.PyAemException(code, message)


def method_not_allowed(response, **kwargs):

	code    = response['http_code']
	soup    = BeautifulSoup(response['body'])
	message = soup.p.string	

	raise exception.PyAemException(code, message)


def unexpected(response, **kwargs):

	code    = response['http_code']
	message = 'Unexpected http code'

	raise exception.PyAemException(code, message)