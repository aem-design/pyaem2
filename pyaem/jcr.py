import bagofrequests as bag
import handlers
import json

class Jcr(object):


	def __init__(self, url, **kwargs):

		self.url      = url
		self.kwargs   = kwargs
		self.handlers = {
			200: handlers.ok_html,
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
