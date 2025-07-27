import asyncio, uuid
from offers_sdk.client import OffersClient
from offers_sdk.models import Product


async def main():
    client = OffersClient(
        refresh_token="REFRESH_TOKEN_FROM_WEB",
        base_url="https://python.exercise.applifting.cz/api/v1"
    )

    print("Is token valid? ", client.auth.is_token_valid())

    # 1. Registering a product
    try:
        new_product = Product(
            id=uuid.uuid4(), name="iPhone", description="Latest Apple smartphone"
        )
        product = await client.register_product(new_product)
        print(f"Product registered: {product}")
    except Exception as e:
        print(f"Registration failed: {e}")
        return  # If the product registration failed, we stop with an error

    # 2. Getting offers
    try:
        offers = await client.get_offers(str(product.id))
        for offer in offers:
            print(
                f"Offer {offer.id}: {offer.price} € (in stock {offer.items_in_stock})"
            )
    except Exception as e:
        print(f"Loading offers failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
