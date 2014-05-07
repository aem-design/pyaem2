class PyAemException(Exception):


    def __init__(self, code, message, response):

        super(PyAemException, self).__init__(message)

        self.code = code
        self.message = message
        self.response = response
