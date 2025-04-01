class InterfaceData:
    def __init__(self, interface_id, host_id, ip, port, mysql_table):
        super().__setattr__('interface_id', interface_id)
        super().__setattr__('host_id', host_id)
        super().__setattr__('ip', ip)
        super().__setattr__('port', port)
        super().__setattr__('_mysql_table', mysql_table)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self._mysql_table.MutexUpdate(f'{name} = {value}', f'interface_id = {self._interface_id}')

class Interface(InterfaceData):
    def __init__(self, interface_id, host_id, ip, port, mysql_table):
        super().__init__(interface_id, host_id, ip, port, mysql_table)

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