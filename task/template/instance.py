import os
from pathlib import Path
import yaml

from task.template.template import (Template)

class Instance:
    def __init__(self, template_path, data_path):
        if not os.path.isfile(template_path):
            raise ValueError(f'Invalid path to template file {template_path}')
        if not os.path.isfile(data_path):
            raise ValueError(f'Invalid path to data file {data_path}')
        template = Path(template_path)
        self.template = Template(template.parent, template.name)
        try:
            with open(data_path, 'r') as f:
                self.data = yaml.safe_load(f.read())
                f.close()
        except Exception as e:
            #TODO: logger
            pass
        self.template.LoadTemplate()
        self.segment_set = self.template.Implement(self.data)