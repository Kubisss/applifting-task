import pytest
import httpx
from uuid import uuid4
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer
from offers_sdk.exceptions import APIError, _raise_for_status

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

            class MockAuthResponse:
                status_code = 200
                text = '{"access_token":"TEST_TOKEN","expires_in":100}'

                def json(self):
                    return {"access_token": "TEST_TOKEN", "expires_in": 100}

                def raise_for_status(self):
                    _raise_for_status(self)

            return MockAuthResponse()

        elif "/products/register" in url:

            class MockProductResponse:
                status_code = 200
                text = '{"id":"%s","name":"%s","description":"%s"}' % (
                    product_sample.id,
                    product_sample.name,
                    product_sample.description,
                )

                def json(self):
                    return {
                        "id": str(product_sample.id),
                        "name": product_sample.name,
                        "description": product_sample.description,
                    }

                def raise_for_status(self):
                    _raise_for_status(self)

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

            def raise_for_status(self):
                _raise_for_status(self)

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    with pytest.raises(APIError):
        await client.register_product(product_sample)


async def test_get_offers(monkeypatch, client, product_sample):
    sample_offers = [
        {"id": str(uuid4()), "price": 999, "items_in_stock": 10},
        {"id": str(uuid4()), "price": 899, "items_in_stock": 5},
    ]

    async def mock_post(*args, **kwargs):
        class MockAuthResponse:
            status_code = 200
            text = '{"access_token":"TEST_TOKEN","expires_in":100}'

            def json(self):
                return {"access_token": "TEST_TOKEN", "expires_in": 100}

            def raise_for_status(self):
                _raise_for_status(self)

        return MockAuthResponse()

    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = '{"access_token":"TEST_TOKEN","expires_in":100}'

            def json(self):
                return sample_offers

            def raise_for_status(self):
                _raise_for_status(self)

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    offers = await client.get_offers(product_sample.id)
    assert len(offers) == 2
    assert isinstance(offers[0], Offer)
    assert offers[0].price == 999


@pytest.mark.asyncio
async def test_register_product_raises_apierror_on_400(mocker, product_sample):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.text = "Invalid input"
    mock_response.raise_for_status = lambda: _raise_for_status(mock_response)

    mock_post = mocker.AsyncMock(return_value=mock_response)
    mocker.patch("httpx.AsyncClient.post", mock_post)

    client = OffersClient(base_url="http://fake.url", refresh_token="FAKE_REFRESH")

    with pytest.raises(APIError) as exc_info:
        await client.register_product(product_sample)

    assert exc_info.value.status_code == 400
    assert "Invalid input" in exc_info.value.response_text
