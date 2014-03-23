from BeautifulSoup import *
import exception
import json

def ok_html(response, **kwargs):

	HEX_MASSAGE = [(re.compile('&#x([^;]+);'), lambda m: '&#%d;' % int(m.group(1), 16))]

	code   = response['http_code']
	soup   = BeautifulSoup(response['body'],
		convertEntities = BeautifulSoup.HTML_ENTITIES,
		markupMassage   = HEX_MASSAGE
	)
	errors = soup.findAll(attrs={ 'class': 'error' })

	if len(errors) == 0:
		result = {
			'status' : 'success',
			'message': 'TODO - where to get success message from'
		}
	else:
		result = {
			'status' : 'failure',
			'message': errors[0].string
		}

	return result


def ok_json(response, **kwargs):

	data    = json.loads(response['body'])
	message = data['msg']

	result = {
		'status' : 'success' if data['success'] == True else 'failure',
		'message': message
	}

	return result


def ok_download_file(response, **kwargs):

	result = {
		'status' : 'success',
		'message': '{0} was successfully downloaded'.format(kwargs['file_name'])
	}

	return result


def ok_upload_file(response, **kwargs):

	data = json.loads(response['body'])

	result = {
		'status' : 'success' if data['success'] == True else 'failure',
		'message': data['msg']
	}

	return result


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