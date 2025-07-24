import pytest
import httpx
import time
from offers_sdk.auth import AuthManager, AuthError

pytestmark = pytest.mark.asyncio


@pytest.fixture
def auth_manager(tmp_path):
    # použijeme dočasný soubor pro cache
    cache_path = tmp_path / ".auth_token.json"
    return AuthManager(refresh_token="FAKE_REFRESH", base_url="http://fake.url", cache_path=str(cache_path))


async def test_get_access_token_success(monkeypatch, auth_manager):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"access_token": "NEW_TOKEN", "expires_in": 100}
            def raise_for_status(self): pass
        return MockResponse()
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    token = await auth_manager.get_access_token()
    assert token == "NEW_TOKEN"
    assert auth_manager.is_token_valid()


async def test_get_access_token_cached(monkeypatch, auth_manager):
    # nastavení starého tokenu
    auth_manager._access_token = "CACHED_TOKEN"
    auth_manager._expires_at = time.time() + 100  # platný

    token = await auth_manager.get_access_token()
    assert token == "CACHED_TOKEN"  # nepoužije mock_post


async def test_refresh_token_error(monkeypatch, auth_manager):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 422
            text = '{"detail":"Invalid token"}'
            def raise_for_status(self): raise httpx.HTTPStatusError("Bad", request=None, response=self)
        return MockResponse()
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    with pytest.raises(AuthError):
        await auth_manager.get_access_token()
