import bagofrequests as bag
from BeautifulSoup import *
import handlers
import json
import re

class ContentRepo(object):


	def __init__(self, url, **kwargs):

		def _handler_ok(response, **kwargs):

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

		self.url      = url
		self.kwargs   = kwargs
		self.handlers = {
			200: _handler_ok,
			401: handlers.auth_fail,
			405: handlers.method_not_allowed
		}


	def activate_tree(self, path, **kwargs):

		params   = {
			'cmd'  : 'activate',
			'path' : path
		}
		method   = 'post'
		url      = '{0}/etc/replication/treeactivation.html'.format(self.url)
		params   = dict(params.items() + kwargs.items())
		handlers = self.handlers
		opts     = self.kwargs

		return bag.request(method, url, params, handlers, **opts)