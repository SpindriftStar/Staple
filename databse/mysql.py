import pymysql
import pymysql.cursors

class MySQLTable:
    def __init__(self, cursor, table_name):
        self.cursor = cursor
        self.table_name = table_name

    def __del__(self):
        self.cursor.close()

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
        return MySQLTable(self.connection.cursor())