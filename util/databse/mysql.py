import pymysql
import pymysql.cursors

class MySQLTable:
    def __init__(self, table_name, key_name, value_name, db):
        self.table_name = table_name
        self.key_name = key_name
        self.value_name = value_name if isinstance(value_name, list) else [value_name]
        self.cursor = db.cursor(cursor = pymysql.cursors.DictCursor)

    def GetTable(self):
        self.cursor.execute('SELECT %s, %s FROM %s' % (self.key_name, ', '.join(self.value_name), self.table_name))
        result = self.cursor.fetchall()
        return result
    
    def GetColumn(self, key):
        self.cursor.execute('SELECT %s FROM %s WHERE %s = %s' % (', '.join(self.value_name), self.table_name, self.key_name,key))
        result = self.cursor.fetchall()
        return result[0] if result else None
    
    def SetColumn(self, key, value):
        self.cursor.execute('UPDATE %s SET %s WHERE %s = %s' % (self.table_name, ', '.join([f'{k} = {v}' for k, v in value.items()]), self.key_name, key))
        return self.cursor.rowcount
    
    def CreateColumn(self, key, value):
        self.cursor.execute('INSERT INTO %s (%s, %s) VALUES (%s, %s)' % (self.table_name, self.key_name, ', '.join(self.value_name), key, ', '.join([f'{v}' for k, v in value.items()])))
        return self.cursor.rowcount
    
    def DeleteColumn(self, key):
        self.cursor.execute('DELETE FROM %s WHERE %s = %s' % (self.table_name, self.key_name, key))
        return self.cursor.rowcount
    
class MySQLDatabase:
    def __init__(self, host, user, password, db_name):
        self.db_name = db_name
        self.connection = pymysql.connect(host = host, user = user, password = password, db = self.db_name)

    def __del__(self):
        self.connection.close()
    
    def GetTable(self, table_name, key_name, value_name):
        return MySQLTable(table_name, key_name, value_name, self.connection)