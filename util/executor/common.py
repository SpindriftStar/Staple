class BaseExecutor:
    def __init__(self, interface, auth):
        self.interface = interface
        self.auth = auth

    def Load(self, command_set):
        raise NotImplementedError("Load method must be implemented in subclasses")

    