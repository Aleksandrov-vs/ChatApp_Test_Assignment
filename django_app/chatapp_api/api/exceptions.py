class AuthorizationError(Exception):
    def __init__(self, message="Authorization error"):
        self.message = message
        super().__init__(self.message)


class PhoneDoesNotExist(Exception):
    def __init__(self, message="Phone does not exist"):
        self.message = message
        super().__init__(self.message)
