from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class KvellError(Exception):
    __code = "kvell_exception"
    __message: str = None
    __error_code: str = None

    def __init__(self, message: str | dict = "", error_code: str = ""):
        self.__message = message
        self.__error_code = error_code

        logger.warning(
            "%s: code: %s; message: %s; kvell_code: %s",
            self.__class__.__name__,
            self.__code,
            self.__message,
            self.__error_code,
        )

    def __repr__(self):
        return f"KVELL exception; code: {self.__code}; message: {self.__message}; error_code: {self.__error_code}"

    def get_code(self):
        return self.__code

    def get_message(self):
        return self.__message

    def get_error_code(self):
        return self.__error_code


class KvellAPIError(KvellError):
    status_code: int
    body: str

    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(message=body, error_code=str(status_code))

    def __repr__(self):
        return f"KvellAPIError: status_code={self.status_code}; body={self.body}"


class KvellValidationError(KvellAPIError):
    errors: list

    def __init__(self, errors: list):
        self.errors = errors
        super().__init__(status_code=422, body=str(errors))

    def __repr__(self):
        return f"KvellValidationError: errors={self.errors}"
