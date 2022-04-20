"""
**********************************************************************************

SQL Command that you can execute:
    select:     SELECT a single row
    selectAll:  SELECT multiple records
    modify:     INSERT, UPDATE, or DELETE commands

**********************************************************************************
"""
from __future__ import annotations
from .structs import DbOperationResult as DbOperationResult
from .connection import ConnectionDict, ConnectionPrepared

#------------------------------------------------------
# Execute a select statement for a single record
#
# Args:
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#------------------------------------------------------
def select(sql_stmt: str, parms: tuple=None) -> DbOperationResult:
    return _selectSteps(False, sql_stmt, parms)


#------------------------------------------------------
# Execute a select statement for a multiple records
#
# Args:
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#------------------------------------------------------
def selectAll(sql_stmt: str, parms: tuple=None) -> DbOperationResult:
    return _selectSteps(True, sql_stmt, parms)


#------------------------------------------------------
# Select command steps
#
# Args:
#   fetch_all: whether or not to select all the records
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#------------------------------------------------------
def _selectSteps(fetch_all: bool, sql_stmt: str, parms: tuple=None) -> DbOperationResult:
    db_result = DbOperationResult(successful=True)
    db = ConnectionDict()

    try:
        db.connect()
        cursor = db.getCursor()
        cursor.execute(sql_stmt, parms)

        if fetch_all:
            db_result.data = cursor.fetchall()
        else:
            db_result.data = cursor.fetchone()
    
    except Exception as e:
        _handleException(db_result, e)
    finally:
        db.close()
    
    return db_result



#------------------------------------------------------
# Execute an insert, update, or delete sql command
#
# Args:
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#
# Returns a DbOperationResult:
#   sets the data field to the row count
#------------------------------------------------------
def modify(sql_stmt: str, parms: tuple=None) -> DbOperationResult:    
    return _modifyCommand(False, sql_stmt, parms)

#------------------------------------------------------
# Execute a batch insert, update, or delete sql command
#
# Args:
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#
# Returns a DbOperationResult:
#   sets the data field to the row count
#------------------------------------------------------
def modifyBatch(sql_stmt: str, parms: list[tuple]=None) -> DbOperationResult:
    return _modifyCommand(True, sql_stmt, parms)


#------------------------------------------------------
# Execute an insert, update, or delete sql command
#
# Args:
#   execute_many: flag indicating to utilize the executemany MySqlCursor routine
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#
# Returns a DbOperationResult:
#   sets the data field to the row count
#------------------------------------------------------
def _modifyCommand(execute_many: bool, sql_stmt: str, parms: tuple | list[tuple]) -> DbOperationResult:
    result = DbOperationResult(successful=True)
    
    db = ConnectionPrepared()

    try:
        db.connect()
        cursor = db.getCursor()

        if execute_many:
            cursor.executemany(sql_stmt, parms)
        else:
            cursor.execute(sql_stmt, parms)
        
        db.commit()
        
        result.data = cursor.rowcount
    except Exception as e:
        _handleException(result, e)
    finally:
        db.close()
    
    return result

#------------------------------------------------------
# Call the specified stored procedure using the given parms
#
# Args:
#   procedure: procedure name
#   parms: a list of parms to pass to the procedure
#
# Returns a DbOperationResult:
#   the data property is set to all the results returned from the procedure
#------------------------------------------------------
def proc(procedure: str, parms: list=None) -> DbOperationResult:
    db_result = DbOperationResult(successful=True)
    connection = ConnectionDict()

    try:
        # connect to the database
        connection.connect()
        mycursor = connection.getCursor()

        # call the stored procedure
        mycursor.callproc(procedure, parms)

        # fetch all the datasets returned from the dataset
        result_data = []
        for stored_result in mycursor.stored_results():
            records = stored_result.fetchall()
            result_data.append(records)

        db_result.data = result_data

        connection.commit()

    except Exception as e:
        db_result.successful = False
        db_result.data       = None
        db_result.error      = e
    
    finally:
        connection.close()
    
    return db_result


#------------------------------------------------------
# Steps to take for an exception raised during an sql command
#------------------------------------------------------
def _handleException(operation_result: DbOperationResult, ex: Exception):
    operation_result.error = ex
    operation_result.data = None
    operation_result.successful = False