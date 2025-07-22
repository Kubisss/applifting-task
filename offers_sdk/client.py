import httpx
from typing import List
from .models import Product, Offer
from .auth import AuthManager


class APIError(Exception):
    # Exception during API calls.
    pass


class OffersClient:
    # Main client for communication with the Offers API.

    def __init__(self, refresh_token: str, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.auth = AuthManager(refresh_token, base_url)

    async def _get_headers(self) -> dict:
        token = await self.auth.get_access_token()
        return {"accept": "application/json", "Bearer": f"{token}", "Content-Type": "application/json"}

    async def register_product(self, product: Product) -> Product:
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/products/register",
                headers=headers,
                json=product.model_dump()
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Error while registering product: {response.text}") from e

            data = response.json()
            return Product(
                id=data.get("id", product.id),
                name=product.name,
                description=product.description
            )


    async def get_offers(self, product_id: str) -> List[Offer]:
        # Returns a list of offers (GET /products/{product_id}/offers).

        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/products/{product_id}/offers",
                headers=headers
            )
        if response.status_code >= 400:
            raise APIError(f"Error while fetching offers: {response.text}")
        return [Offer(**offer) for offer in response.json()]
