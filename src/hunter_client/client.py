"""Hunter.io API client with functional programming techniques."""

from functools import lru_cache
from typing import Any, Callable, Optional, TypeVar

import httpx
from pydantic import ValidationError

from hunter_client.models import (
    AccountInformationResponse,
    DomainSearchResponse,
    EmailFinderResponse,
    EmailVerifierResponse,
)

ResponseType = TypeVar("ResponseType")


class HunterAPIError(Exception):
    """Custom exception for Hunter API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        """Initialize the exception."""
        super().__init__(message)
        self.status_code = status_code


def handle_response(
    response_model: type[ResponseType],
) -> Callable[[httpx.Response], ResponseType]:
    """Create a handler for API responses."""

    def process_response(response: httpx.Response) -> ResponseType:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            error_msg = "HTTP error occurred: {0}".format(exc.response.text)
            raise HunterAPIError(error_msg, exc.response.status_code) from exc

        try:
            json_data = response.json()
        except Exception as exc:
            error_msg = "Unexpected error: {0}".format(exc)
            raise HunterAPIError(error_msg) from exc

        try:
            if "data" in json_data:
                return response_model(**json_data["data"])
            return response_model(**json_data)
        except ValidationError as exc:
            error_msg = "Validation error: {0}".format(exc)
            raise HunterAPIError(error_msg) from exc

    return process_response


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose functions from right to left."""

    def composed_function(arg: Any) -> Any:
        current_result = arg
        for func in reversed(functions):
            current_result = func(current_result)
        return current_result

    return composed_function


class HunterClient:
    """Hunter.io API client."""

    BASE_URL = "https://api.hunter.io/v2"

    def __init__(self, api_key: str, timeout: float = 30.0) -> None:
        """Initialize the Hunter.io client."""
        self.api_key = api_key
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=timeout,
            params={"api_key": api_key},
        )

    def __enter__(self) -> "HunterClient":
        """Enter context manager."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    @lru_cache(maxsize=128)
    def _cached_get(self, endpoint: str, params_str: str) -> httpx.Response:
        """Make cached GET request."""
        request_params = dict(pair.split("=") for pair in params_str.split("&") if pair)
        return self._client.get(endpoint, params=request_params)

    def _make_request(
        self,
        endpoint: str,
        request_params: Optional[dict[str, Any]] = None,
    ) -> httpx.Response:
        """Make a GET request to the API."""
        request_params = request_params or {}
        params_str = "&".join(
            "{0}={1}".format(key, val) for key, val in sorted(request_params.items()) if val is not None
        )
        return self._cached_get(endpoint, params_str)

    def domain_search(
        self,
        domain: str,
        email_type: Optional[str] = None,
        seniority: Optional[str] = None,
        department: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DomainSearchResponse:
        """Search for emails by domain."""
        request_params = {
            "domain": domain,
            "type": email_type,
            "seniority": seniority,
            "department": department,
            "limit": limit,
            "offset": offset,
        }

        response = self._make_request("/domain-search", request_params)
        handler = handle_response(DomainSearchResponse)
        return handler(response)

    def email_finder(
        self,
        domain: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        full_name: Optional[str] = None,
    ) -> EmailFinderResponse:
        """Find email address."""
        if not (full_name or (first_name and last_name)):
            raise ValueError(
                "Either full_name or both first_name and last_name must be provided",
            )

        request_params = {
            "domain": domain,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
        }

        response = self._make_request("/email-finder", request_params)
        handler = handle_response(EmailFinderResponse)
        return handler(response)

    def email_verifier(self, email: str) -> EmailVerifierResponse:
        """Verify an email address."""
        request_params = {"email": email}

        response = self._make_request("/email-verifier", request_params)
        handler = handle_response(EmailVerifierResponse)
        return handler(response)

    def account_information(self) -> AccountInformationResponse:
        """Get account information."""
        response = self._make_request("/account")
        handler = handle_response(AccountInformationResponse)
        return handler(response)


def create_client(api_key: str, timeout: float = 30.0) -> HunterClient:
    """Create a Hunter client instance."""
    return HunterClient(api_key=api_key, timeout=timeout)
