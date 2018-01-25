import mysql.connector


class DatabaseConnect(object):
    def __init__(self):
        self.connection_string = mysql.connector.connect(host='127.0.0.1', database='mwdb_p1'
                                                         , user='root', password='root')

    def getCursorForDatabase(self):
        return self.connection_string.cursor()

    def closeDatabaseConnection(self):
        self.connection_string.close()
