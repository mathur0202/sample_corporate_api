class BaseError(Exception):
    def __init__(self, message):
        self.message = {'error': message}


class ValidationError(BaseError):
    pass


class ObjectNotFoundError(BaseError):
    pass


class UnauthorisedError(BaseError):
    pass


class ForbiddenError(BaseError):
    pass


class DmgAppError(BaseError):
    pass