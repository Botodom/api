class BotodomApiError(Exception):
    """API Error"""

    def __init__(self, message: str = "", type: str = ""):
        self.message = message
        self.type = type
        super().__init__(self.message, self.type)


class BadRequest(BotodomApiError):
    """Bad Request"""

    def __init__(self, message: str = "", type: str = ""):
        super().__init__(message, type)

class NotFound(BotodomApiError):
    """Not Found"""

    def __init__(self, message: str = "", type: str = ""):
        super().__init__(message, type)