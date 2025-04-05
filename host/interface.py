from database.mysql import (DataLoader)

class Interface():
    def __init__(self, data):
        self.data = data

class InterfaceContainer:
    def __init__(self, database):
        dataloader = DataLoader(database, 'interface', 'interface_id', ['description', 'host_id', 'ip', 'port'])
        self.interfaces = {}
        for interface_id, data in dataloader:
            self.interfaces[interface_id] = Interface(data)

    def __getitem__(self, interface_id):
        return self.interfaces[interface_id]

    def __delitem__(self, interface_id):
        del self.interfaces[interface_id]

    def __iter__(self):
        self.interface_iter = iter(self.interfaces.items())
        return self
    
    def __next__(self):
        return next(self.interface_iter)
    
    def __len__(self):
        return self.interfaces.__len__()