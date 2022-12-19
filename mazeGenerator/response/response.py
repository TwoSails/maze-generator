from typing import Any


class Response:
    __slots__ = ["success", "data", "error"]

    def __init__(self, success: bool, data: Any, error) -> None:
        self.success = success
        self.data = data
        self.error = error

    def __repr__(self):
        if self.success:
            return f"Ok<{self.data}>"
        return f"Err<{self.error}>"
        # return f"Response<{self.success=}, {self.data=}, {self.error=}>"


class Ok(Response):
    def __init__(self, data=None) -> None:
        super().__init__(True, data, None)


class Err(Response):
    def __init__(self, err=None, data=None) -> None:
        super().__init__(False, data, err)
