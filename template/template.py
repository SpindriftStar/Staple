import os
import glob
from jinja2 import Environment, FileSystemLoader

class Template:
    def __init__(self, template_dir):
        self.template_dir = template_dir

    def __iter__(self):
        self.files = glob.glob(os.path.join(self.template_dir, '*.xml'))
        self.count = 0
        return self
    
    def __next__(self):
        if self.count == len(self.files):
            raise StopIteration
        file = self.files[self.count]
        self.count += 1
        return os.path.basename(file)

    def __len__(self):
        return len(self.files)