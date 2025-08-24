"""Response handling for Hunter.io API."""

from typing import Any, TypeVar

import httpx
from pydantic import ValidationError

ResponseType = TypeVar('ResponseType')


class HunterAPIError(Exception):
    """Custom exception for Hunter API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize the exception."""
        super().__init__(message)
        self.status_code = status_code


def parse_json_response(response: httpx.Response) -> dict[str, Any]:
    """Parse JSON from response."""
    try:
        return response.json()
    except Exception as error:
        error_msg = 'Failed to parse JSON: {0}'.format(error)
        raise HunterAPIError(error_msg) from error


def extract_model_data(json_data: dict[str, Any]) -> dict[str, Any]:
    """Extract model data from JSON response."""
    data_value = json_data.get('data')
    return data_value if data_value is not None else json_data


def validate_response_model(
    json_data: dict[str, Any],
    response_model: type[ResponseType],
) -> ResponseType:
    """Validate and create response model."""
    model_data = extract_model_data(json_data)
    try:
        return response_model(**model_data)
    except ValidationError as error:
        error_msg = 'Validation error: {0}'.format(error)
        raise HunterAPIError(error_msg) from error


def check_http_status(response: httpx.Response) -> None:
    """Check HTTP status and raise error if needed."""
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        error_msg = 'HTTP error occurred: {0}'.format(error.response.text)
        raise HunterAPIError(error_msg, error.response.status_code) from error


def process_api_response(
    response: httpx.Response,
    response_model: type[ResponseType],
) -> ResponseType:
    """Process API response and return model instance."""
    check_http_status(response)
    json_data = parse_json_response(response)
    return validate_response_model(json_data, response_model)
