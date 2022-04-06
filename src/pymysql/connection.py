import mysql.connector
from mysql.connector.cursor import MySQLCursor, MySQLCursorPrepared, MySQLCursorDict
from . import credentials as db_credentials


class ConnectionBase:
    """A MySQL database connection"""

    #----------------------------------------------------------
    # Constructor
    #----------------------------------------------------------
    def __init__(self):
        self.connection = mysql.connector.MySQLConnection()
    
    #----------------------------------------------------------
    # Connect to the database
    #----------------------------------------------------------
    def connect(self):
        self.connection = mysql.connector.connect(
            user     = db_credentials.USER,
            host     = db_credentials.HOST,
            database = db_credentials.DATABASE,
            password = db_credentials.PASSWORD
        )
    
    #----------------------------------------------------------
    # Close the database connection
    #----------------------------------------------------------
    def close(self):
        self.connection.close()

    #----------------------------------------------------------
    # Commit the current transaction
    #----------------------------------------------------------
    def commit(self):
        self.connection.commit()
        
    #----------------------------------------------------------
    # Get a cursor from the database connection.
    #
    # Args:
    #     a_dbCursorType (DbCursorTypes): Cursor type
    #
    # Returns:
    #     MySQLCursor: The connected mysql cursor.
    #----------------------------------------------------------
    def getCursor(self) -> MySQLCursor:
        return self.connection.cursor()



class ConnectionPrepared(ConnectionBase):

    #----------------------------------------------------------
    # Return a prepared cursor
    #----------------------------------------------------------
    def getCursor(self) -> MySQLCursorPrepared:
        return self.connection.cursor(prepared=True)

class ConnectionDict(ConnectionBase):

    #----------------------------------------------------------
    # Return a dictionary cursor
    #----------------------------------------------------------
    def getCursor(self) -> MySQLCursorDict:
        return self.connection.cursor(dictionary=True)


