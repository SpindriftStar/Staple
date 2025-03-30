import os
from pathlib import Path

import paramiko

from executor.common import (BaseExecutor)

class SSHAuth:
    def __init__(self, device_id, use_password, username, passward, key):
        self.device_id = device_id
        self.use_password = use_password
        self.username = username
        self.password = passward
        self.key = key

        if key != '' and use_password == 0:
            if not isinstance(key, paramiko.RSAKey) and isinstance(key, str):
                try:
                    self.key = paramiko.RSAKey.from_private_key_file(key)
                except Exception as e:
                    raise ValueError(f'Cannot read SSH key file {key}') from e
            else:
                raise TypeError('Invalid SSH key file')

class SSHBaseExecutor(BaseExecutor):
    def __init__(self, interface, auth):
        super().__init__(interface)
        self.auth = auth
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if self.auth.use_password == 1:
                # Use password-based authentication
                self.ssh_client.connect(hostname = self.interface.ip,
                                        port = self.interface.port, 
                                        username = self.auth.username,
                                        password = self.auth.password)
            else:
                # Use key-based authentication
                self.ssh_client.connect(hostname = self.interface.ip,
                                        port = self.interface.port, 
                                        username = self.auth.username,
                                        pkey = self.auth.key)
        except Exception as e:
            raise e

    def Execute(self, command = None, params = None):
        pass

    def __del__(self):
        self.ssh_client.close()

class SSHShellExecutor(SSHBaseExecutor):
    def __init__(self, interface, auth):
        super().__init__(interface, auth)
    
    def Execute(self, command = None, params = None):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return (stdin.read().decode(), stdout.read().decode(), stderr.read().decode())

class SFTPExecutor(SSHBaseExecutor):
    def __init__(self, interface, auth):
        super().__init__(interface, auth)
        self.SFTP_client = self.ssh_client.open_sftp()
        
    def Execute(self, command = None, params = None):
        params = params if isinstance(params, list) else [params]
        try:
            if command == 'get':
                for param in params:
                    remote_path = param[0]
                    local_path = param[1]
            if command == 'put':
                for param in params:
                    local_path = param[0]
                    remote_path = param[1]
            if command == 'ls':
                for param in params:
                    dir_path = param
            if command == 'mkdir':
                for param in params:
                    dir_path = param
            if command == 'rm':
                for param in params:
                    file_path = param
            if command == 'rmdir':
                for param in params:
                    dir_path = params
        except Exception as e:
            raise e

    def __del__(self):
        self.SFTP_client.close()