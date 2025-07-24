import pytest
import httpx
from uuid import uuid4
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer

pytestmark = pytest.mark.asyncio


@pytest.fixture
def client():
    return OffersClient(refresh_token="FAKE", base_url="http://fake.url")


@pytest.fixture
def product_sample():
    return Product(id=uuid4(), name="iPhone", description="Latest Apple smartphone")


async def test_register_product(monkeypatch, client, product_sample):
    async def mock_post(self, url, *args, **kwargs):
        if url.endswith("/auth"):
            # Mock odpovědi pro získání tokenu
            class MockAuthResponse:
                status_code = 200
                def json(self):
                    return {"access_token": "TEST_TOKEN", "expires_in": 100}
                def raise_for_status(self): pass
            return MockAuthResponse()
        elif "/products/register" in url:
            # Mock odpovědi pro registraci produktu
            class MockProductResponse:
                status_code = 200
                def json(self):
                    return {
                        "id": str(product_sample.id),
                        "name": product_sample.name,
                        "description": product_sample.description
                    }
                def raise_for_status(self): pass
            return MockProductResponse()
        else:
            raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    product = await client.register_product(product_sample)
    assert product.id == product_sample.id
    assert product.name == "iPhone"
    assert product.description == "Latest Apple smartphone"

async def test_register_product_error(monkeypatch, client, product_sample):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 400
            text = "Bad Request"
            def raise_for_status(self): raise httpx.HTTPStatusError("Bad", request=None, response=self)
        return MockResponse()
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    with pytest.raises(Exception):
        await client.register_product(product_sample)


async def test_get_offers(monkeypatch, client, product_sample):
    sample_offers = [
        {"id": str(uuid4()), "price": 999, "items_in_stock": 10},
        {"id": str(uuid4()), "price": 899, "items_in_stock": 5}
    ]

    async def mock_post(*args, **kwargs):
        # Mock pro získání access tokenu
        class MockAuthResponse:
            status_code = 200
            def json(self): return {"access_token": "TEST_TOKEN", "expires_in": 100}
            def raise_for_status(self): pass
        return MockAuthResponse()

    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self): return sample_offers
            def raise_for_status(self): pass
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    offers = await client.get_offers(product_sample.id)
    assert len(offers) == 2
    assert isinstance(offers[0], Offer)
    assert offers[0].price == 999
