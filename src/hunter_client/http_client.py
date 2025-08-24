"""Base HTTP client for Hunter.io API."""

from typing import Any, Optional

import httpx

from hunter_client.config import CACHE_SIZE, DEFAULT_TIMEOUT, HUNTER_API_BASE_URL


class BaseHTTPClient:
    """Base HTTP client with common functionality."""

    def __init__(self, api_key: str, timeout: float = DEFAULT_TIMEOUT) -> None:
        """Initialize the HTTP client."""
        self.api_key = api_key
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=HUNTER_API_BASE_URL,
            timeout=timeout,
            params={'api_key': api_key},
        )
        self._cache: dict[str, httpx.Response] = {}

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()
        self._cache.clear()

    def get(
        self,
        endpoint: str,
        request_params: Optional[dict[str, Any]] = None,
        use_cache: bool = True,
    ) -> httpx.Response:
        """Make a GET request."""
        request_params = request_params or {}

        # Create cache key from sorted params
        cache_key = self._create_cache_key(endpoint, request_params)

        # Check cache if enabled
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        # Make request
        clean_params = self._clean_params(request_params)
        response = self._client.get(endpoint, params=clean_params)

        # Cache response if enabled
        if use_cache:
            self._manage_cache(cache_key, response)

        return response

    def _clean_params(self, request_params: dict[str, Any]) -> dict[str, Any]:
        """Remove None values from parameters."""
        return {key: params_value for key, params_value in request_params.items() if params_value is not None}

    def _create_cache_key(self, endpoint: str, request_params: dict[str, Any]) -> str:
        """Create a cache key from endpoint and params."""
        sorted_params = sorted(request_params.items())
        params_str = '&'.join(
            '{0}={1}'.format(key, param_value) for key, param_value in sorted_params if param_value is not None
        )
        return '{0}?{1}'.format(endpoint, params_str)

    def _manage_cache(self, key: str, response: httpx.Response) -> None:
        """Manage cache size and add new entry."""
        if len(self._cache) >= CACHE_SIZE:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key)
        self._cache[key] = response
