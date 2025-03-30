class Host:
    def __init__(self, host_id, name, interface, status, accessible):
        self.host_id = host_id
        self.name = name
        self.interface = interface if isinstance(interface, (list, tuple)) else [interface]
        self.status = status
        self.accessible = accessible