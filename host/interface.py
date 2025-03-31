class Interface:
    def __init__(self, interface_id, host_id, ip, port, mysql_table):
        self._interface_id = interface_id
        self.host_id = host_id
        self.ip = ip
        self.port = port

        self._mysql_table = mysql_table

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self._mysql_table.Update(f'{name} = {value}', f'interface_id = {self._interface_id}')

    @property
    def interface_id(self):
        return self._interface_id
    
class InterfaceContainer:
    def __init__(self, mysql_database):
        self._mysql_table = mysql_database.GetTable('interface')

        self._interfaces = {}
        interfaces = self._mysql_table.FetchAll()
        for (interface_id, host_id, ip, port) in interfaces:
            self._interfaces[interface_id] = Interface(interface_id, host_id, ip, port, self._mysql_table)

    def __getitem__(self, interface_id):
        return self._interfaces[interface_id]

    def __delitem__(self, interface_id):
        del self._interfaces[interface_id]

    def __iter__(self):
        self._interface_ids = self._interfaces.keys()
        self._interface_ids.__iter__()
        return self
    
    def __next__(self):
        interface_id = self._interface_ids.__next__()
        return interface_id, self._interfaces[interface_id]
    
    def __len__(self):
        return self._interfaces.__len__()