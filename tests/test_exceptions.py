import pytest
from offers_sdk.exceptions import (
    _raise_for_status,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ServerError,
    APIError,
)


class DummyResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


@pytest.mark.parametrize(
    "status, expected_exception, expected_message",
    [
        (400, BadRequestError, "Invalid request."),
        (401, UnauthorizedError, "Unauthorized."),
        (403, ForbiddenError, "Forbidden."),
        (404, NotFoundError, "Not found."),
        (409, ConflictError, "Conflict."),
        (500, ServerError, "Server error."),
        (502, ServerError, "Server error."),
        (
            418,
            APIError,
            "Unhandled client error.",
        ),  # 418 je nějaký 4xx co nemáš explicitně ošetřený
    ],
)
def test_raise_for_status_raises_correct_exceptions(
    status, expected_exception, expected_message
):
    response = DummyResponse(status, "Error body text")
    exc = None
    with pytest.raises(expected_exception) as e:
        _raise_for_status(response)
    exc = e.value
    assert exc.status_code == status
    assert exc.response_text == "Error body text"
    assert expected_message in str(exc)


def test_raise_for_status_does_not_raise_for_success():
    response = DummyResponse(200, "OK")
    # nemělo by vyhodit žádnou výjimku
    _raise_for_status(response)
