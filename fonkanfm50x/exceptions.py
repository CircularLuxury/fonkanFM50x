class UnexpectedReaderResponseException(Exception):
    pass

class TagReadException(Exception):
    pass

# <Error code> 0: other error 3: memory overrun 4: memory locked B: Insufficient power F: Non-specific error

# written ok <error code> 0: other error 3: memory overrun 4: memory locked   B: Insufficient power F: Non-specific error Z00~Z1F: words write 3Z00~3Z1F: error code and words write

# kill ok <error code> 0: other error 3: memory overrun 4: memory locked   B: Insufficient power F: Non-specific error
# lock ok <error code> 0: other error 3: memory overrun 4: memory locked B: Insufficient power F: Non-specific error