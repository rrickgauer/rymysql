"""
**********************************************************************************
Name:       credentials

Purpose:    variables containing the login credentials for the datbase server.
**********************************************************************************
"""

USER     = None
PASSWORD = None
DATABASE = None
HOST     = None

# set the credentials from a dictionary
def fromDict(credentialsDict: dict):
    global USER, PASSWORD, DATABASE, HOST
    
    USER     = credentialsDict.get('user')
    PASSWORD = credentialsDict.get('password')
    DATABASE = credentialsDict.get('database')
    HOST     = credentialsDict.get('host')
