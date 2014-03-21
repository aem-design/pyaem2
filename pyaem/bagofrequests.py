import requests

def req(method, url, params, auth, handlers, **kwargs):

	allow_redirects = kwargs['allow_redirects'] if 'allow_redirects' in kwargs else True
	files           = kwargs['files'] if 'files' in kwargs else None
	stream          = kwargs['stream'] if 'stream' in kwargs else False
	timeout         = kwargs['timeout'] if 'timeout' in kwargs else 30000
	verify          = kwargs['verify'] if 'timeout' in kwargs else False

	response = requests.request(method, url,
		allow_redirects = allow_redirects,
		auth            = auth,
		files           = files,
		params          = params,
		stream          = stream,
		timeout         = timeout,
		verify          = verify
	)

	if response.status_code in handlers:
		return handlers[response.status_code](response, **kwargs)
	else:
		return handlers['unexpected'](response, **kwargs)