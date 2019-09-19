SUCCESS = 'success'
FAILURE = 'failure'
WARNING = 'warning'

class PyAem2Result():


    def __init__(self, response):

        self.response = response
        self.status = None
        self.message = None


    def success(self, message):

        self.status = SUCCESS
        self.message = message


    def failure(self, message):

        self.status = FAILURE
        self.message = message


    def warning(self, message):

        self.status = WARNING
        self.message = message


    def is_success(self):

        return self.status == SUCCESS


    def is_failure(self):

        return self.status == FAILURE


    def is_warning(self):

        return self.status == WARNING


    def debug(self):

        data = {
            'Request method': self.response['request']['method'],
            'Request URL': self.response['request']['url'],
            'Request parameters': self.response['request']['params'],
            'Response code': self.response['http_code'],
            'Response body': self.response['body'],
            'Result status': self.status,
            'Result message': self.message
        }

        debug = ''
        for key in data:
            debug += '{0}: {1}\n'.format(key, data[key])

        return debug
