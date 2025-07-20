import pytest
from offers_sdk.client import OffersClient

@pytest.mark.asyncio
async def test_ping():
    client = OffersClient("dummy-token", "https://fake.api")
    assert await client.ping() == "SDK is alive"