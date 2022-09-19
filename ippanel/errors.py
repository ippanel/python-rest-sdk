import enum

from ippanel.models import Response


class ResponseCode(enum.Enum):
    ErrForbidden = 403
    ErrNotFound = 404
    ErrUnprocessableEntity = 422
    ErrInternalServer = 500


class Error(Exception):
    """
    Error template
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

        super(Error, self).__init__(str(message))


class HTTPError(Exception):
    pass

def parse_errors(response: Response):
    if response.code != 200 or response.error_message != '':
        return Error(response.code, response.error_message)
    return
