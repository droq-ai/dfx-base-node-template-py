"""HTTP client helper for making API requests."""

import asyncio
import json
import logging
import os
from typing import Any, Dict, Optional

import aiohttp


logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client wrapper for making API requests."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize HTTP client.

        Args:
            base_url: Base URL for API (defaults to BASE_URL env var)
            timeout: Request timeout in seconds
            headers: Default headers for all requests
        """
        self.base_url = base_url or os.getenv("BASE_URL", "")
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.default_headers = headers or {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def start(self) -> None:
        """Start HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers=self.default_headers,
            )
            logger.info("HTTP client session started")

    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("HTTP client session closed")

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from base URL and endpoint."""
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return endpoint

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data as dictionary
        """
        if not self.session:
            await self.start()

        url = self._build_url(endpoint)
        request_headers = {**self.default_headers, **(headers or {})}

        try:
            async with self.session.get(url, params=params, headers=request_headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"GET request failed: {e}")
            raise

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make POST request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers

        Returns:
            Response data as dictionary
        """
        if not self.session:
            await self.start()

        url = self._build_url(endpoint)
        request_headers = {**self.default_headers, **(headers or {})}

        try:
            if json_data:
                async with self.session.post(
                    url, json=json_data, headers=request_headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            else:
                async with self.session.post(
                    url, data=data, headers=request_headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"POST request failed: {e}")
            raise

    async def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make PUT request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers

        Returns:
            Response data as dictionary
        """
        if not self.session:
            await self.start()

        url = self._build_url(endpoint)
        request_headers = {**self.default_headers, **(headers or {})}

        try:
            if json_data:
                async with self.session.put(
                    url, json=json_data, headers=request_headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            else:
                async with self.session.put(
                    url, data=data, headers=request_headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"PUT request failed: {e}")
            raise

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make DELETE request.

        Args:
            endpoint: API endpoint
            headers: Additional headers

        Returns:
            Response data as dictionary
        """
        if not self.session:
            await self.start()

        url = self._build_url(endpoint)
        request_headers = {**self.default_headers, **(headers or {})}

        try:
            async with self.session.delete(url, headers=request_headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"DELETE request failed: {e}")
            raise

