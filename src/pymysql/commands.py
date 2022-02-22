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
    result = DbOperationResult(successful=True)
    
    db = ConnectionPrepared()

    try:
        db.connect()
        cursor = db.getCursor()
        cursor.execute(sql_stmt, parms)
        db.commit()
        
        result.data = cursor.rowcount
    except Exception as e:
        _handleException(result, e)
    finally:
        db.close()
    
    return result


#------------------------------------------------------
# Steps to take for an exception raised during an sql command
#------------------------------------------------------
def _handleException(operation_result: DbOperationResult, ex: Exception):
    operation_result.error = ex
    operation_result.data = None
    operation_result.successful = False