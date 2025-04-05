import os
from pathlib import Path

import re

from database.mysql import (DataLoader)

class ContentIter:
    def __init__(self, dir, file):
        if os.path.isdir(dir):
            file_path = os.path.join(dir, file)
            if os.path.isfile(file_path):
                self.dir = dir
                self.file = Path(file_path)
            else:
                raise ValueError(f'Invalid path to template file {file_path}')
        else:
            raise ValueError(f'Invalid directory to template file {dir}')
        
    def __iter__(self):
        lines = self.file.read_text().splitlines()
        self.current_iter = iter(lines)
        self.last_iter = None
        return self
    
    def __next__(self):
        try:
            line = next(self.current_iter)
            line_split = line.split(' ')
            prefix = line_split[0]
            if prefix == '__IMPORT__':
                if len(line_split) != 2:
                    raise ValueError(f'Invalid import statement {line}')
                file = line_split[1]
                content_iter = ContentIter(self.dir, file)
                self.last_iter = self.current_iter
                self.current_iter = iter(content_iter)
                return next(self.current_iter)
            else:
                return line
        except StopIteration as e:
            if self.last_iter is  None:
                raise StopIteration from e
            else:
                self.current_iter = self.last_iter
                self.last_iter = None
                return next(self.current_iter)

class Template:
    def __init__(self, data):
        self.data = data
        file = Path(self.data.file)
        self.dir = file.parent
        self.filename = file.name
        
        self.lines = []

    def LoadTemplate(self):
        for line in ContentIter(self.dir, self.filename):
            #line_split = line.split(' ')
            #prefix = line_split[0]
            self.lines.append(('__EXE__', line))

    def Implement(self, data: dict):
        def replace_with_dict(match):
            return data[match.group(1)]
        pattern = r'{{(.*?)}}'
        return [re.sub(pattern, replace_with_dict, line) for line in self.lines]
    
class ImpTemplate:
    def __init__(self, lines):
        self.lines = lines

    def Parse(self):
        self.parsed_lines = self.lines
        
    def __iter__(self):
        self.Parse()
        self.line_iter = iter(self.parsed_lines)
        return self
    
    def __next__(self):
        return next(self.line_iter)
    
class TemplateContainer:
    def __init__(self, database):
        dataloader = DataLoader(database, 'template', 'template_id', ['description', 'status', 'file'])
        self.templates = {}
        for template_id, data in dataloader:
            self.templates[template_id] = Template(data)

    def __getitem__(self, template_id):
        return self.templates[template_id]

    def __delitem__(self, template_id):
        del self.templates[template_id]

    def __iter__(self):
        self.template_iter = iter(self.templates.items())
        return self
    
    def __next__(self):
        return next(self.template_iter)
    
    def __len__(self):
        return self.templates.__len__()