"""Service classes for Hunter.io API operations."""

from typing import Any, Optional

from hunter_client.endpoints import (
    HunterEndpoints,
    build_domain_search_params,
    build_email_finder_params,
)
from hunter_client.http_client import BaseHTTPClient
from hunter_client.models.account import AccountInformationResponse
from hunter_client.models.domain import DomainSearchParams, DomainSearchResponse
from hunter_client.models.email_finder import EmailFinderResponse
from hunter_client.models.verifier import EmailVerifierResponse
from hunter_client.response_handler import process_api_response


class DomainService:
    """Service for domain-related operations."""

    def __init__(self, client: BaseHTTPClient) -> None:
        """Initialize domain service."""
        self._client = client

    def search_with_params(self, search_params: DomainSearchParams) -> DomainSearchResponse:
        """Search for emails by domain using params object."""
        request_params = build_domain_search_params(search_params)
        response = self._client.get(HunterEndpoints.domain_search.path, request_params)
        return process_api_response(response, DomainSearchResponse)

    def search(self, **kwargs: Any) -> DomainSearchResponse:
        """Search for emails by domain.

        Accepts keyword arguments matching DomainSearchParams fields:
        domain, email_type, seniority, department, limit, offset.
        """
        search_params = DomainSearchParams(**kwargs)
        return self.search_with_params(search_params)


class EmailService:
    """Service for email-related operations."""

    def __init__(self, client: BaseHTTPClient) -> None:
        """Initialize email service."""
        self._client = client

    def find(
        self,
        domain: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        full_name: Optional[str] = None,
    ) -> EmailFinderResponse:
        """Find email address."""
        request_params = build_email_finder_params(domain, first_name, last_name, full_name)
        response = self._client.get(HunterEndpoints.email_finder.path, request_params)
        return process_api_response(response, EmailFinderResponse)

    def verify(self, email: str) -> EmailVerifierResponse:
        """Verify an email address."""
        request_params = {'email': email}
        response = self._client.get(HunterEndpoints.email_verifier.path, request_params)
        return process_api_response(response, EmailVerifierResponse)


class AccountService:
    """Service for account-related operations."""

    def __init__(self, client: BaseHTTPClient) -> None:
        """Initialize account service."""
        self._client = client

    def get_information(self) -> AccountInformationResponse:
        """Get account information."""
        response = self._client.get(HunterEndpoints.account.path)
        return process_api_response(response, AccountInformationResponse)
