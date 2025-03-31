class Interface:
    def __init__(self, interface_id, host_id, ip, port, mysql_table):
        self._interface_id = interface_id
        self.host_id = host_id
        self.ip = ip
        self.port = port

        self._mysql_table = mysql_table

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self._mysql_table.Update(f'{name} = {value}', f'interface_id = {self.interface_id}')

    @property
    def interface_id(self):
        return self._interface_id