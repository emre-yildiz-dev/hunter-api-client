"""Basic tests for Hunter.io client."""

import pytest

from hunter_client.client import HunterClient, create_client
from hunter_client.response_handler import HunterAPIError


def test_create_client():
    """Test client creation."""
    client = create_client(api_key="test_key")
    assert isinstance(client, HunterClient)
    assert client._http_client.api_key == "test_key"
    client.close()


def test_client_context_manager():
    """Test client works as context manager."""
    with create_client(api_key="test_key") as client:
        assert isinstance(client, HunterClient)
        assert hasattr(client, "domain")
        assert hasattr(client, "email")
        assert hasattr(client, "account")


def test_hunter_api_error():
    """Test custom exception."""
    error = HunterAPIError("Test error", status_code=404)
    assert str(error) == "Test error"
    assert error.status_code == 404


def test_client_services_exist():
    """Test that all services are properly initialized."""
    client = create_client(api_key="test_key")

    # Check services exist
    assert client.domain is not None
    assert client.email is not None
    assert client.account is not None

    # Check service methods exist
    assert hasattr(client.domain, "search")
    assert hasattr(client.email, "find")
    assert hasattr(client.email, "verify")
    assert hasattr(client.account, "get_information")

    client.close()
