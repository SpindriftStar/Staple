import os
from pathlib import Path
import yaml

from task.executor.ssh import (SSHShellExecutor, SFTPExecutor)
from database.mysql import (DataLoader)

class Instance:
    def __init__(self, data, imp_template, executor):
        self.data = data
        self.executor = executor
        self.imp_template = imp_template

    def Run(self):
        for line in self.imp_template:
            prefix = line[0]
            if prefix == '__EXE__':
                command = line[1]
                self.executor.Execute(command)

class InstanceContainer:
    def __init__(self, database, host_container, interface_container, auth_container, template_container):
        dataloader = DataLoader(database, 'instance', 'instance_id', ['host_id', 'template_id', 'interface_id', 'auth_id', 'description', 'status', 'implement', 'executor'])
        self.instances = {}
        for instance_id, data in dataloader:
            interface = interface_container[data.interface_id]
            auth = auth_container[data.auth_id]
            host = host_container[data.host_id]
            template = template_container[data.template_id]

            template.LoadTemplate()
            imp_template = template.Implement(data.implement)

            executor = self.CreateExecutor(data.executor, host, interface, auth)

            self.instances[instance_id] = Instance(data, imp_template, executor)

    def CreateExecutor(self, executor_type, host, interface, auth):
        if executor_type == 0:
            return SSHShellExecutor(interface, auth)
        elif executor_type == 1:
            return SFTPExecutor(interface, auth)
        else:
            raise ValueError(f'Invalid executor type {executor_type}')