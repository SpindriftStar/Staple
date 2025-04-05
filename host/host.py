from database.mysql import (DataLoader)

class Host:
    def __init__(self, data):
        self.data = data
    
class HostContainer:
    def __init__(self, database):
        dataloader = DataLoader(database, 'host', 'host_id', ['name', 'status', 'accessible'])
        self.hosts = {}
        for host_id, data in dataloader:
            self.hosts[host_id] = Host(data)

    def __getitem__(self, host_id):
        return self.hosts[host_id]

    def __delitem__(self, host_id):
        del self.hosts[host_id]

    def __iter__(self):
        self.host_iter = iter(self.hosts.items())
        return self
    
    def __next__(self):
        return next(self.host_iter)
    
    def __len__(self):
        return self.hosts.__len__()