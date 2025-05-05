class BaseExecutor:
    def __init__(self, interface, auth):
        self.interface = interface
        self.auth = auth

    def Load(self, command_set):
        raise NotImplementedError("Load method must be implemented in subclasses")

    def __iter__(self):
        raise NotImplementedError("Subclasses must implement __iter__ method")
    
    def __next__(self):
        raise NotImplementedError("Subclasses must implement __next__ method")
    
    def __len__(self):
        raise NotImplementedError("Subclasses must implement __len__ method")