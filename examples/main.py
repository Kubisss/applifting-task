import asyncio
from offers_sdk.client import OffersClient

async def main():
    client = OffersClient(refresh_token="YOUR_TOKEN", base_url="https://offers.api")
    print(await client.ping())

if __name__ == "__main__":
    asyncio.run(main())
