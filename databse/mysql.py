import pymysql

class MySQLFetchIter:
    def __init__(self, cursor, query, params=None):
        self.cursor = cursor
        self.cursor.execute(query, params)

    def __iter__(self):
        return self

    def __next__(self):
        row = self.cursor.fetchone()
        if row is None:
            raise StopIteration
        return row

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
            self.cursor = self.connection.cursor()
        except Exception as e:
            assert False, f"Failed to connect to database: {e}"

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def ExecuteQuery(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def FetchAll(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def FetchIter(self, query, params=None):
        return MySQLFetchIter(self.cursor, query, params)