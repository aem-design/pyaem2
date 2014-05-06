SUCCESS = 'success'
FAILURE = 'failure'
WARNING = 'warning'

class PyAemResult(object):


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
