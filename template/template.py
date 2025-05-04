import os
import glob
from jinja2 import Environment, FileSystemLoader

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

    def GetFile(self, file_name):
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