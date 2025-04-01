class HostData:
    def __init__(self, host_id, name, status, accessible, mysql_table):
        super().__setattr__('host_id', host_id)
        super().__setattr__('name', name)
        super().__setattr__('status', status)
        super().__setattr__('accessible', accessible)
        super().__setattr__('_mysql_table', mysql_table)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self._mysql_table.Update(f'{name} = {value}', f'host_id = {self._host_id}')

class Host:
    def __init__(self, host_id, name, interface, status, accessible, mysql_table):
        self.data = HostData(host_id, name, status, accessible, mysql_table)
        self.interface = interface if isinstance(interface, (list, tuple)) else [interface]
    
class HostContainer:
    def __init__(self, mysql_database):
        self._mysql_table = mysql_database.GetTable('host')

        self._hosts = {}
        hosts = self._mysql_table.FetchAll()
        for (host_id, name, interface, status, accessible) in hosts:
            self._hosts[host_id] = Host(host_id, name, interface, status, accessible, self._mysql_table)

    def __getitem__(self, host_id):
        return self._hosts[host_id]

    def __delitem__(self, host_id):
        del self._hosts[host_id]

    def __iter__(self):
        self._host_ids = self._hosts.keys()
        self._host_ids.__iter__()
        return self
    
    def __next__(self):
        host_id = self._host_ids.__next__()
        return host_id, self._hosts[host_id]
    
    def __len__(self):
        return self._hosts.__len__()