class TriggerData:
    def __init__(self, trigger_id, expression, description, status, priority, task_id, mysql_table):
        super().__setattr__('trigger_id', trigger_id)
        super().__setattr__('expression', expression)
        super().__setattr__('description', description)
        super().__setattr__('status', status)
        super().__setattr__('priority', priority)
        super().__setattr__('task_id', task_id)
        super().__setattr__('_mysql_table', mysql_table)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self._mysql_table.Update(f'{name} = {value}', f'trigger_id = {self.trigger_id}')

class Trigger():
    def __init__(self, trigger_id, expression, description, status, priority, task_id, mysql_table):
        self.data = TriggerData(trigger_id, expression, description, status, priority, task_id, mysql_table)

    def ParseExpression(self):
        expression = self.data.expression
        expression_split = expression.split(' ')
        prefix = expression_split[0]
        if prefix == '@restart':
            self._type = 0
            self._times = 1
            self._timedelta = -1
            self._signal = 'signal_restart'
        elif prefix == '@interval':
            if len(expression_split) != 5:
                raise ValueError(f'Invalid trigger expression {expression}')
            if not (str.isnumeric(expression_split[1]) 
            and str.isnumeric(expression_split[2]) 
            and str.isnumeric(expression_split[3]) 
            and str.isnumeric(expression_split[4])):
                raise ValueError(f'Invalid time expression in trigger expression {expression}')
            self._type = 1
            self._times = int(expression_split[1])
            second = int(expression_split[2])
            minute = int(expression_split[3])
            hour = int(expression_split[4])
            self._timedelta = second + minute * 60 + hour * 3600
            self._signal = 'signal_interval'
        elif prefix == '@signal':
            signals = expression_split[1:]
            if len(signals) != 1:
                raise ValueError(f'No valid signal in trigger expression {expression}')
            self._type = 2
            self._times = -1
            self._timedelta = -1
            self._signal = signals[0]
        else:
            raise ValueError(f'Invalid trigger expression {expression}')