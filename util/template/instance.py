from template.template import Template
from executor.ssh import SSHExecutor

class Instance:
    def __init__(self, template, args):
        self.template = template
        self.args = args
    
    def Build(self, interface, auth):
        self.template.Render(self.args)
        meta = self.ParseXML()
        self.name = meta['name']
        self.description = meta['description']
        executors = meta['executors']
        preprocessing = meta['preprocessing']
        triggers = meta['triggers']

        self.executors = []
        self.preprocessings = []
        self.triggers = []