class HandlersMatcher():

    def __init__(self, handler_keys):
        self.handler_keys = handler_keys

    def __eq__(self, handlers):
        return list(handlers.keys()).sort() == self.handler_keys.sort()
