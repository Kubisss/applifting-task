import httpx


class OffersSDKError(Exception):
    # Basic exception for all errors Offers SDK.
    pass


class APIError(OffersSDKError):
    # General error when calling the API.

    def __init__(
        self, message: str, status_code: int = None, response_text: str = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

    def __str__(self):
        base = super().__str__()
        if self.status_code is not None:
            return f"{base} (status code: {self.status_code})"
        return base


class BadRequestError(APIError):
    # HTTP 400 – Bad Request.
    pass


class UnauthorizedError(APIError):
    # HTTP 401 – Unauthorized.
    pass


class ForbiddenError(APIError):
    # HTTP 403 – Forbidden.
    pass


class NotFoundError(APIError):
    # HTTP 404 – Not Found.
    pass


class ConflictError(APIError):
    # HTTP 409 – Conflict.
    pass


class ServerError(APIError):
    # HTTP 5xx – Server Error.
    pass


def _raise_for_status(response: httpx.Response):
    status = response.status_code
    text = response.text

    if status == 400:
        raise BadRequestError(
            "Invalid request.", status_code=status, response_text=text
        )
    elif status == 401:
        raise UnauthorizedError("Unauthorized.", status_code=status, response_text=text)
    elif status == 403:
        raise ForbiddenError("Forbidden.", status_code=status, response_text=text)
    elif status == 404:
        raise NotFoundError("Not found.", status_code=status, response_text=text)
    elif status == 409:
        raise ConflictError("Conflict.", status_code=status, response_text=text)
    elif status >= 500:
        raise ServerError("Server error.", status_code=status, response_text=text)
    elif status >= 400:
        raise APIError(
            "Unhandled client error.", status_code=status, response_text=text
        )
