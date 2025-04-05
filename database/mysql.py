import pymysql
import pymysql.cursors

from concurrent.futures import ThreadPoolExecutor

class Data:
    def __init__(self, id_name, id, data : dict, table):
        super().__setattr__(id_name, id)
        for key, value in data.items():
            super().__setattr__(key, value)
        super().__setattr__('_table', table)
        super().__setattr__('_id_name', id_name)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self._table.MutexUpdate(f'{name} = {value}', f'{self._id_name} = {self.__dict__[self._id_name]}')

class DataLoader:
    def __init__(self, database, table_name, id_key, data_key):
        table = database.GetTable(table_name)

        self.data = {}
        value = table.FetchAll()
        for id, *data in value:
            self.data[id] = Data(id_key, id, dict(zip(data_key, data)), table)
        
    def __iter__(self):
        self.data_iter = iter(self.data.items())
        return self
    
    def __next__(self):
        return next(self.data_iter)
    
    def __getitem__(self, id):
        return self.data[id]

class MySQLTable:
    def __init__(self, cursor, table_name, thread_pool_executor = None):
        self.cursor = cursor
        self.table_name = table_name
        if thread_pool_executor is not None:
            self.thread_pool_executor = thread_pool_executor

    def __del__(self):
        self.cursor.close()

    def FetchOne(self, condition = None):
        if condition is None:
            self.cursor.execute('SELECT * FROM %s', self.table_name)
        else:
            self.cursor.execute('SELECT * FROM %s WHERE %s', (self.table_name, condition))
        return self.cursor.fetchone()

    def FetchAll(self, condition = None):
        if condition is None:
            self.cursor.execute('SELECT * FROM %s', self.table_name)
        else:
            self.cursor.execute('SELECT * FROM %s WHERE %s', (self.table_name, condition))
        return self.cursor.fetchall()
    
    def Update(self, expression, condition):
        self.cursor.execute('UPDATE %s SET %s WHERE %s', (self.table_name, expression, condition))
        return self.cursor.commit()
    
    def Delete(self, condition):
        self.cursor.execute('DELETE FROM %s WHERE %s', (self.table_name, condition))
        return self.cursor.commit()
    
    def MutexFetchOne(self, condition = None):
        future = self.thread_pool_executor.submit(self.FetchOne, condition)
        return future.result()
    
    def MutexFetchAll(self, condition = None):
        future = self.thread_pool_executor.submit(self.FetchAll, condition)
        return future.result()
    
    def MutexUpdate(self, expression, condition, result = False):
        future = self.thread_pool_executor.submit(self.Update, expression, condition)
        if result:
            return future.result()
        else:
            return None
        
    def MutexDelete(self, condition, result = False):
        future = self.thread_pool_executor.submit(self.Delete, condition)
        if result:
            return future.result()
        else:
            return None

class MySQLDatabase():
    def __init__(self, host, port, user, password, database):
        try:
            self.connection = pymysql.connect(
                host = host,
                port = port,
                user = user,
                password = password,
                database = database
            )
        except Exception as e:
            assert False, f"Failed to connect to database: {e}"

    def __del__(self):
        self.connection.close()

    def GetTable(self, table_name):
        return MySQLTable(self.connection.cursor(), table_name)