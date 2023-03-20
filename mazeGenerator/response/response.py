from typing import Any


class Response:
    """
    Super class to contain data from the return value of an operation
    Used to improve data flow management
    """
    __slots__ = ["success", "data", "error"]

    def __init__(self, success: bool, data: Any, error) -> None:
        self.success = success
        self.data = data
        self.error = error

    def __repr__(self):
        if self.success:
            return f"Ok<{self.data}>"
        return f"Err<{self.error}>"


class Ok(Response):
    """
    Success response
    """
    def __init__(self, data=None) -> None:
        super().__init__(True, data, None)


class Err(Response):
    """
    Erroneous response
    """
    def __init__(self, err=None, data=None) -> None:
        super().__init__(False, data, err)
