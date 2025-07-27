import httpx
import time
from typing import Optional

from offers_sdk.exceptions import _raise_for_status
from .token_cache import TokenCache


class AuthError(Exception):
    pass


class AuthManager:
    # Takes care about access token:
    # - Loading from cache (file .auth_token.json),
    # - Checking validity according to timestamp,
    # - On expiration (or if not present) calls /auth (header 'Bearer': <refresh_token>),
    # - Saving new token + expiration back to cache.

    def __init__(
        self, refresh_token: str, base_url: str, cache_path: str = ".auth_token.json"
    ):
        self.refresh_token = refresh_token
        self.base_url = base_url.rstrip("/")
        self.cache = TokenCache(cache_path)

        # loaded
        self._access_token, self._expires_at = (
            self.cache.load()
        )  # expires_at: float timestamp

    async def get_access_token(self, skew: float = 30.0) -> str:
        # Returns valid access token. If token is not present or has expired calls /auth and restore it.

        if self.is_token_valid(skew=skew):
            return self._access_token

        await self._refresh_access_token()
        return self._access_token

    def is_token_valid(self, skew: float = 30.0) -> bool:
        # True, if token exists and did not expire (with time buffer `skew` in seconds).

        if not self._access_token:
            return False
        now = time.time()
        return now < (self._expires_at - skew)

    def token_valid_for(self) -> float:
        return self._expires_at - time.time()

    async def _refresh_access_token(self):
        print("[Auth DEBUG] Requesting new token...")

        url = f"{self.base_url}/auth"
        headers = {"Bearer": self.refresh_token}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)

        if response.status_code >= 400:
            _raise_for_status(response)

        data = response.json()
        self._access_token = data["access_token"]

        expires_in = data.get("expires_in", 300)
        self._expires_at = time.time() + float(expires_in) - 30

        self.cache.save(self._access_token, self._expires_at)
        print(f"[Auth DEBUG] New token saved.")
