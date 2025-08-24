"""Dependency functions for Hunter.io API client."""

import os

from fastapi import HTTPException

from hunter_client.client import HunterClient, create_client
from hunter_client.config import HTTP_ERROR_CODE


def get_client() -> HunterClient:
    """Get Hunter.io client instance."""
    api_key = os.getenv('HUNTER_API_KEY')
    if not api_key:
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail='HUNTER_API_KEY environment variable not set',
        )
    return create_client(api_key)
