import paramiko

from executor.common import BaseExecutor

class BaseSSHExecutor(BaseExecutor):
    def __init__(self, interface, auth):
        super().__init__(interface, auth)
        ip = interface.ip
        port = interface.port

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if auth.use_password == 1:
            username = auth.username
            password = auth.password
            self.client.connect(ip, port = port, username = username, password = password)
        elif auth.use_password == 0:
            key_filename = auth.key_filename
            self.client.connect(ip, port = port, username = auth.username, key_filename = key_filename)
        else:
            raise ValueError("Invalid authentication method specified. Use 0 for key-based or 1 for password-based authentication.")
        
    def Load(self, command_set):
        raise NotImplementedError("Load method must be implemented in subclasses")

    def __iter__(self):
        raise NotImplementedError("Subclasses must implement __iter__ method")
    
    def __next__(self):
        raise NotImplementedError("Subclasses must implement __next__ method")
    
    def __len__(self):
        raise NotImplementedError("Subclasses must implement __len__ method")
    
    def Close(self):
        self.client.close()

class SSHExecutor(BaseSSHExecutor):
    def __init__(self, interface, auth):
        super().__init__(interface, auth)
        self.command_set = None

    def Load(self, command_set):
        self.command_set = command_set
        self.len = len(command_set)

    def __iter__(self):
        self.count = 0
        return self
    
    def __next__(self):
        if self.count == self.len:
            raise StopIteration
        command = self.command_set[self.count]
        stdin, stdout, stderr = self.client.exec_command(command)
        self.count += 1
        return (stdin, stdout, stderr)
    
    def __len__(self):
        return self.len