class Host:
    def __init__(self, host_id, name, interface, status, accessible, mysql_table):
        self._host_id = host_id
        self.name = name
        self.interface = interface if isinstance(interface, (list, tuple)) else [interface]
        self.status = status
        self.accessible = accessible

        self._mysql_table= mysql_table

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name != 'interface':
            self._mysql_table.Update(f'{name} = {value}', f'host_id = {self._host_id}')

    @property
    def host_id(self):
        return self._host_id
    
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