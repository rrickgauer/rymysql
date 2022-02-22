"""
**********************************************************************************

Some database structures/models used throughout the application.

**********************************************************************************
"""

from dataclasses import dataclass
from typing import Any

#----------------------------------------------------------
# This class is used when a function executes a database command.
# It is a way to standardize the outcome of an sql operation.
#----------------------------------------------------------
@dataclass
class DbOperationResult:
    successful: bool = False
    data      : Any  = None
    error     : Exception  = None






