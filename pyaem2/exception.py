class PyAem2Exception(Exception):


    def __init__(self, code, message, response):

        super(PyAem2Exception, self).__init__(message)

        self.code = code
        self.message = message
        self.response = response
