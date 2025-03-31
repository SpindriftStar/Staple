import pymysql
import pymysql.cursors

from concurrent.futures import ThreadPoolExecutor

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
    
    def MutFetchOne(self, condition = None):
        future = self.thread_pool_executor.submit(self.FetchOne, condition)
        return future.result()
    
    def MutFetchAll(self, condition = None):
        future = self.thread_pool_executor.submit(self.FetchAll, condition)
        return future.result()
    
    def MutUpdate(self, expression, condition, result = False):
        future = self.thread_pool_executor.submit(self.Update, expression, condition)
        if result:
            return future.result()
        else:
            return None
        
    def MutDelete(self, condition, result = False):
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