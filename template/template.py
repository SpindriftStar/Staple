import os
import glob
from jinja2 import Environment, FileSystemLoader
from xml.etree import ElementTree as ET

class Template:
    def __init__(self, env, template_name):
        self.env = env
        self.template_name = template_name
        self.template = env.get_template(template_name)

    def Render(self, args):
        self.impl_template = self.template.render(args)

    def LoadXML(self):
        self.tree = ET.ElementTree(ET.fromstring(self.impl_template))
        self.root = self.tree.getroot()
        if self.root is None:
            raise ValueError("Invalid XML format")
        return self.root
    
    def ParseXML(self):
        self.template.Render(self.args)
        xml_root = self.template.LoadXML()
        if xml_root.tag != 'instance':
            raise ValueError("Invalid XML format")

        meta = {}
        name = xml_root.find('name')
        description = xml_root.find('description')
        executors = xml_root.find('executors')
        preprocessing = xml_root.find('preprocessing')
        triggers = xml_root.find('triggers')
     
        if name is None:
            raise ValueError("Missing name tag")
        if description is None:
            raise ValueError("Missing description tag")
        if executors is None:
            raise ValueError("Missing executors tag")
        if preprocessing is None:
            raise ValueError("Missing preprocessing tag")
        if triggers is None:
            raise ValueError("Missing triggers tag")

        meta['name'] = name.text
        meta['description'] = description.text

        meta['executors'] = []
        for executor in executors:
            if executor.tag == 'SSH':
                command_set = []
                commands = executor.findall('command')
                if not commands:
                    raise ValueError("Missing command tag in executors.SSH")
                for command in commands:
                    command_set.append((command.get('key'), command.text))
                meta['executors'].append({'type': executor.tag, 'command': command_set})
            else:
                raise ValueError(f"Unknown tag in executors: {executor.tag}")

        meta['preprocessing'] = []
        steps = preprocessing.findall('step')
        if steps is None:
            raise ValueError("Missing step tag in preprocessing")
        for step in steps:
            type = step.find('type')
            if type is None:
                raise ValueError("Missing type tag in step")
            if type.text == 'JAVASCRIPT':
                params = step.findall('param')
                expression = step.find('expression')
                output = step.find('output')
                if params is None:
                    raise ValueError("Missing param tag in step")
                if expression is None:
                    raise ValueError("Missing expression tag in step")
                if output is None:
                    raise ValueError("Missing output tag in step")
                param_set = []
                for param in params:
                    param_set.append(param.text)
                expression = expression.text
                output = output.text
                meta['preprocessing'].append({'type': 'JAVASCRIPT', 'params': param_set, 'expression': expression, 'output': output})
            else:
                raise ValueError(f"Unknown type in step: {type.text}")

        meta['triggers'] = []
        triggers = triggers.findall('trigger')
        if triggers is None:
            raise ValueError("Missing trigger tag in triggers")
        for trigger in triggers:
            expression = trigger.find('expression')
            message = trigger.find('message')
            level = trigger.find('level')
            if expression is None:
                raise ValueError("Missing expression tag in trigger")
            if message is None:
                raise ValueError("Missing message tag in trigger")
            if level is None:
                raise ValueError("Missing level tag in trigger")
            expression = expression.text
            message = message.text
            level = level.text
            meta['triggers'].append({'expression': expression, 'message': message, 'level': level})
        return meta

class TemplateManager:
    def __init__(self, template_dir):
        self.template_dir = template_dir
        self.env = Environment(loader = FileSystemLoader(template_dir))
        self.files = [os.path.basename(file) for file in sorted(glob.glob(os.path.join(self.template_dir, '*.xml')))]
        self.num_files = len(self.files)

    def __iter__(self):
        self.count = 0
        return self
    
    def __next__(self):
        if self.count == self.num_files:
            raise StopIteration
        file = self.files[self.count]
        self.count += 1
        return file

    def __len__(self):
        return self.num_files
    
    def NewFile(self, file_name, content):
        if not file_name.endswith('.xml'):
            raise ValueError("File name must end with .xml")
        if file_name in self.files:
            raise ValueError("File already exists")
        with open(os.path.join(self.template_dir, file_name), 'w') as f:
            f.write(content)
        self.files = sorted(self.files.append(file_name))
        self.num_files = len(self.files)

    def DeleteFile(self, file_name):
        if file_name not in self.files:
            raise ValueError("File not found")
        os.remove(os.path.join(self.template_dir, file_name))
        self.files.remove(file_name)
        self.num_files = len(self.files)

    def ReadFile(self, file_name):
        if file_name not in self.files:
            raise ValueError("File not found")
        with open(os.path.join(self.template_dir, file_name), 'r') as f:
            return f.read()
        
    def WriteFile(self, file_name, content):
        if file_name not in self.files:
            raise ValueError("File not found")
        with open(os.path.join(self.template_dir, file_name), 'w') as f:
            f.write(content)

    def RenderTemplate(self, template_name, **kwargs):
        if template_name not in self.files:
            raise ValueError("File not found")
        template = self.env.get_template(template_name)
        return template.render(**kwargs)