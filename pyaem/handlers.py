from BeautifulSoup import *

def ok_html(response, **kwargs):

	soup   = BeautifulSoup(response.text)
	errors = soup.findAll(attrs={ 'class': 'error' })

	if len(errors) == 0:
		return response.text
	else:
		raise Exception(errors[0].string)

def ok_json(response, **kwargs):

	result = response.json()

	if result['success'] == True:
		return result['msg']
	else:
		raise Exception(result['msg'])

def ok_file(response, **kwargs):

	with open(kwargs['file'], 'wb') as fd:
		for chunk in response.iter_content(1024):
			fd.write(chunk)
		return '{0} was successfully uploaded'.format(kwargs['file'])

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

	# TODO: pretty-print json and html
	if debug == True:
		print 'Response status code {0}\nResponse text:{1}\n'.format(str(response.status_code), str(response.text))