class UnexpectedReaderResponseException(Exception):
    pass

class ReaderCommandNotSupportedException(Exception):
    pass

#################################################
# Tag Read/Write Exceptions
#################################################
class TagGenericException(Exception):
    pass

class TagMemoryOverrunException(TagGenericException):
    pass
class TagMemoryLockedException(TagGenericException):
    pass
class TagInsufficientPowerException(TagGenericException):
    pass
class TagUnknownException(TagGenericException):
    pass

def raise_exception_from_code(error_code: str, message: str = ""):
    if error_code == '3':
        raise TagMemoryOverrunException(message)
    elif error_code == '4':
        raise TagMemoryLockedException(message)
    elif error_code == 'B':
        raise TagInsufficientPowerException(message)
    elif error_code == 'E':
        raise TagUnknownException(message)
    elif error_code == 'F':
        raise TagUnknownException(message)
    elif error_code == '0':
        raise TagGenericException(message)
    else:
        raise UnexpectedReaderResponseException(f"Unknown error code: {error_code}: {message}")
