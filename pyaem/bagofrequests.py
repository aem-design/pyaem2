import requests

def req(method, url, params, auth, handlers, **kwargs):

	response = getattr(requests, method)(url, auth=auth, params=params)

	if response.status_code in handlers:
		handlers[response.status_code](response, debug=kwargs['debug'])
	else:
		handlers['unexpected'](response, debug=kwargs['debug'])