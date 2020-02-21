from enum import Enum


class ErrorCode(Enum):
    NOT_FOUND = {'status_code': 404, 'code': 'NOT_FOUND'}
    TOKEN_EXPIRED = {'status_code': 502, 'code': 'TOKEN_EXPIRED'}
    INTERNAL_SERVER_ERROR = {'status_code': 500, 'code': 'INTERNAL_SERVER_ERROR'}
    INITIALISATION_ERROR = {'status_code': 500, 'code': 'INITIALISATION_ERROR'}
    BAD_REQUEST = {'status_code': 400, 'code': 'BAD_REQUEST'}
    FORBIDDEN = {'status_code': 403, 'code': 'FORBIDDEN'}


class GenericException(Exception):
    def __init__(self, exception=None, error_code: ErrorCode = None, message: str = None):
        self.exception = exception
        if error_code:
            self.error_code = error_code
        else:
            self.error_code = self._map_error_code()
        self.message = message

    def format(self):
        err = {
            'code': self.error_code.name,
        }

        if self.exception:
            err['error'] = self.exception.args[0]

        if self.message:
            err['message'] = self.message
        return err

    def _map_error_code(self):
        if self.exception.args[0].startswith('An error occurred (EntityNotFoundException)'):
            return ErrorCode.NOT_FOUND

        if self.exception.args[0].startswith('An error occurred (ExpiredTokenException)'):
            return ErrorCode.NOT_FOUND

        return ErrorCode.INTERNAL_SERVER_ERROR


class InternalServerErrorException(GenericException):
    def __init__(self, message: str = None):
        super().__init__(None, ErrorCode.INTERNAL_SERVER_ERROR, message)


class BadRequestException(GenericException):
    def __init__(self, message: str = None):
        super().__init__(None, ErrorCode.BAD_REQUEST, message)


class ForbiddenException(GenericException):
    def __init__(self, message: str = None):
        super().__init__(None, ErrorCode.FORBIDDEN, message)


class NotFoundException(GenericException):
    def __init__(self, message: str = None):
        super().__init__(None, ErrorCode.NOT_FOUND, message)
