import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from utils.index import RedBlackTree

class EventManager:
    def __init__(self):
        self.lock = threading.RLock()
        self.signals = RedBlackTree()
        self.scheduler = self.GetScheduler()

    @staticmethod
    def GetScheduler():
        jobstores = {'default': MemoryJobStore()}
        executors = {'default': ThreadPoolExecutor(10)}
        return BackgroundScheduler(jobstores = jobstores, executors = executors)

    @staticmethod
    def SignalHash(signal):
        return hash(signal)

    def Register(self, signal, task, timedelta = -1, data = None):
        if signal == 'signal_restart':
            self.scheduler.add_job(func = task.execute(), args = [data])
        elif signal == 'signal_interval':
            if timedelta > 0:
                self.scheduler.add_job(func = task.execute(), trigger = 'interval', seconds = timedelta, args = [data])
            else:
                raise ValueError('Invalid timedelta')
            
        hash = self.SignalHash(signal)
        self.signals.Append(hash, task)