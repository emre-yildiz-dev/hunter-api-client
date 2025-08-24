"""Hunter.io API client."""

from typing import Any

from hunter_client.config import DEFAULT_TIMEOUT
from hunter_client.http_client import BaseHTTPClient
from hunter_client.response_handler import HunterAPIError  # noqa: F401
from hunter_client.services import AccountService, DomainService, EmailService


class HunterClient:
    """Hunter.io API client with service-based architecture."""

    def __init__(self, api_key: str, timeout: float = DEFAULT_TIMEOUT) -> None:
        """Initialize the Hunter.io client."""
        self._http_client = BaseHTTPClient(api_key, timeout)
        self.domain = DomainService(self._http_client)
        self.email = EmailService(self._http_client)
        self.account = AccountService(self._http_client)

    def __enter__(self) -> 'HunterClient':
        """Enter context manager."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()


def create_client(api_key: str, timeout: float = DEFAULT_TIMEOUT) -> HunterClient:
    """Create a Hunter client instance."""
    return HunterClient(api_key=api_key, timeout=timeout)
