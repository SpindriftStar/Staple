import os
from pathlib import Path

import re

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
        
        self.lines = []

    def LoadTemplate(self):
        for line in ContentIter(self.dir, self.file):
            line_split = line.split(' ')
            prefix = line_split[0]
            if prefix == '__ENV__':
                env = {}
                for statement in line_split[1:]:
                    statement_split = statement.split('=')
                    if len(statement_split) != 2:
                        raise ValueError('No valid assignment statement')
                    env_name = statement_split[0]
                    env_value = statement_split[1]
                    env[env_name] = env_value
                self.lines.append(('__ENV__', env))
            else:
                self.lines.append(('__EXE__', line))
    
    def Implement(self, data: dict):
        def replace_with_dict(match):
            return data[match.group(1)]
        pattern = r'{{(.*?)}}'
        self.implines = [re.sub(pattern, replace_with_dict, line) for line in self.lines]

    def __iter__(self):
        self.line_iter = iter(self.implines)
        return self
    
    def __next__(self):
        return next(self.line_iter)
    
    def __len__(self):
        return len(self.implines)