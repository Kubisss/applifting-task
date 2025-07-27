from urllib import response
import httpx
from typing import List
from .models import Product, Offer
from .auth import AuthManager
from .exceptions import _raise_for_status


class OffersClient:
    # Main client for communication with the Offers API.
    def __init__(self, refresh_token: str, base_url: str):
        clean_token = refresh_token.strip()
        self.refresh_token = clean_token
        self.base_url = base_url.rstrip("/")
        self.auth = AuthManager(clean_token, base_url)

    async def _get_headers(self) -> dict:
        token = await self.auth.get_access_token()
        return {
            "accept": "application/json",
            "Bearer": f"{token}",
            "Content-Type": "application/json",
        }

    async def register_product(self, product: Product) -> Product:
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/products/register",
                headers=headers,
                json=product.model_dump(),
            )
            _raise_for_status(response)

            data = response.json()
            return Product(
                id=data.get("id", product.id),
                name=product.name,
                description=product.description,
            )

    async def get_offers(self, product_id: str) -> List[Offer]:
        # Returns a list of offers (GET /products/{product_id}/offers).

        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/products/{product_id}/offers", headers=headers
            )
        _raise_for_status(response)
        return [Offer(**offer) for offer in response.json()]
