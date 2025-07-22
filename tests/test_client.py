import pytest
import httpx
import asyncio
from offers_sdk.client import OffersClient
from offers_sdk.models import Product
from uuid import uuid4

# Pytest plugin pro async testy
pytestmark = pytest.mark.asyncio

@pytest.fixture
def product_sample():
    return Product(
        id=uuid4(),
        name="iPhone",
        description="Latest Apple smartphone"
    )

async def test_register_product(monkeypatch, product_sample):
    # Mock transport simuluje odpověď serveru
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return {"id": str(product_sample.id)}
        return MockResponse()

    # Monkeypatch httpx.AsyncClient.post
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    client = OffersClient(refresh_token="FAKE", base_url="http://fake.url")
    product = await client.register_product(product_sample)

    assert product.id == product_sample.id
    assert product.name == "iPhone"
