class OffersClient:
    def __init__(self, refresh_token: str, base_url: str):
        self.refresh_token = refresh_token
        self.base_url = base_url

    async def ping(self) -> str:
        return "SDK is alive"
