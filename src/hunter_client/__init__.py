"""Hunter.io API Client Package."""

from hunter_client.client import HunterAPIError, HunterClient, create_client
from hunter_client.models import (
    AccountInformationResponse,
    DomainSearchResponse,
    Email,
    EmailFinderResponse,
    EmailSource,
    EmailVerifierResponse,
)

__version__ = "0.1.0"

__all__ = [
    "HunterClient",
    "HunterAPIError",
    "create_client",
    "DomainSearchResponse",
    "EmailFinderResponse",
    "EmailVerifierResponse",
    "AccountInformationResponse",
    "Email",
    "EmailSource",
]
