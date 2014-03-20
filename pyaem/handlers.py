from BeautifulSoup import *
import json

def ok_json(response, **kwargs):

	result = json.loads(response.text)

	if result['success'] == True:
		return result['msg']
	else:
		raise Exception(result['msg'])

def auth_fail(response, **kwargs):

	_debug(response, kwargs['debug'])
	raise Exception('Authentication failed - incorrect username and/or password')

def auth_required(response, **kwargs):

	_debug(response, kwargs['debug'])
	raise Exception('Authentication required - set username and password')

def method_not_allowed(response, **kwargs):

	soup  = BeautifulSoup(response.text)
	error = soup.p.string

	_debug(response, kwargs['debug'])
	raise Exception(error)

def unexpected(response, **kwargs):

	_debug(response, True)
	raise Exception('Unexpected status code')

def _debug(response, debug):

	if debug == True:
		print 'Response status code {0}\nResponse text:{1}\n'.format(str(response.status_code), str(response.text))