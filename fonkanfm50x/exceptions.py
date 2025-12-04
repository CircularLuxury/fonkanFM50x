class UnexpectedReaderResponseException(Exception):
    pass


#################################################
# Read Exceptions
#################################################
class TagReadGenericException(Exception):
    pass

class TagReadMemoryOverrunException(TagReadGenericException):
    pass
class TagReadMemoryLockedException(TagReadGenericException):
    pass
class TagReadInsufficientPowerException(TagReadGenericException):
    pass
class TagReadUnknownException(TagReadGenericException):
    pass

def raise_exception_from_code_read(error_code: str, message: str = ""):
    if error_code == '3':
        raise TagReadMemoryOverrunException(message)
    elif error_code == '4':
        raise TagReadMemoryLockedException(message)
    elif error_code == 'B':
        raise TagReadInsufficientPowerException(message)
    elif error_code == 'F':
        raise TagReadUnknownException(message)
    elif error_code == '0':
        raise TagReadGenericException(message)
    else:
        raise TagReadGenericException(f"Unknown error code: {error_code}")


#################################################
# Write Exceptions
#################################################
class TagWriteGenericException(Exception):
    pass

class TagWriteMemoryOverrunException(TagWriteGenericException):
    pass
class TagWriteMemoryLockedException(TagWriteGenericException):
    pass
class TagWriteInsufficientPowerException(TagWriteGenericException):
    pass
class TagWriteUnknownException(TagWriteGenericException):
    pass

def raise_exception_from_code_write(error_code: str, message: str = ""):
    if error_code == '3':
        raise TagWriteMemoryOverrunException(message)
    elif error_code == '4':
        raise TagWriteMemoryLockedException(message)
    elif error_code == 'B':
        raise TagWriteInsufficientPowerException(message)
    elif error_code == 'F':
        raise TagWriteUnknownException(message)
    elif error_code == '0':
        raise TagWriteGenericException(message)
    else:
        raise TagWriteGenericException(f"Unknown error code: {error_code}")