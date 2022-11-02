class Response:
    def __init__(self, success: bool, data) -> None:
        self.success = success
        self.data = data

class Ok(Response):
    def __init__(self, data) -> None:
        super().__init__(True, data)

class Err(Response):
    def __init__(self, err) -> None:
        super().__init__(False, err)