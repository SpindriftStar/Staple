from host.host import (Host)

class BaseExecutor:
    def __init__(self, interface, auth):
        self.interface = interface
        self.auth = auth

    def Execute(self, command = None, params = None):
        raise NotImplementedError('Execute method not implemented by subclass')