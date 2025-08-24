"""API endpoint definitions for Hunter.io."""

from dataclasses import dataclass
from typing import Any, Optional

from hunter_client.models.domain import DomainSearchParams


@dataclass
class EndpointConfig:
    """Configuration for an API endpoint."""

    path: str
    method: str = 'GET'


class HunterEndpoints:
    """Hunter.io API endpoints."""

    domain_search = EndpointConfig('/domain-search')
    email_finder = EndpointConfig('/email-finder')
    email_verifier = EndpointConfig('/email-verifier')
    account = EndpointConfig('/account')


def build_domain_search_params(search_params: DomainSearchParams) -> dict[str, Any]:
    """Build parameters for domain search from model."""
    return {
        'domain': search_params.domain,
        'type': search_params.email_type,
        'seniority': search_params.seniority,
        'department': search_params.department,
        'limit': search_params.limit,
        'offset': search_params.offset,
    }


def build_email_finder_params(
    domain: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    full_name: Optional[str] = None,
) -> dict[str, Any]:
    """Build parameters for email finder."""
    if not (full_name or (first_name and last_name)):
        raise ValueError(
            'Either full_name or both first_name and last_name must be provided',
        )

    return {
        'domain': domain,
        'first_name': first_name,
        'last_name': last_name,
        'full_name': full_name,
    }
