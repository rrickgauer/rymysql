"""
**********************************************************************************
Name:       credentials

Purpose:    variables containing the login credentials for the datbase server.
**********************************************************************************
"""

from dataclasses import dataclass


USER     = None
PASSWORD = None
DATABASE = None
HOST     = None


@dataclass
class ConnectionCredentials:
    user    : str = None
    password: str = None
    database: str = None
    host    : str = None

#----------------------------------------------------------
# Set the credentials from the given dictionary.
#
# The keys in the dict are:
#   - user
#   - password
#   - database
#   - host
#----------------------------------------------------------
def fromDict(credentialsDict: dict):
    global USER, PASSWORD, DATABASE, HOST
    
    USER     = credentialsDict.get('user') or None
    PASSWORD = credentialsDict.get('password') or None
    DATABASE = credentialsDict.get('database') or None
    HOST     = credentialsDict.get('host') or None


#----------------------------------------------------------
# Set the credentials from the given ConnectionCredentials object
#----------------------------------------------------------
def fromObject(connection_credentials: ConnectionCredentials):
    global USER, PASSWORD, DATABASE, HOST
    
    USER     = connection_credentials.user
    PASSWORD = connection_credentials.password
    DATABASE = connection_credentials.database
    HOST     = connection_credentials.host
