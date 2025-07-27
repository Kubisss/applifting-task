import json
from pathlib import Path
from typing import Optional, Tuple


class TokenCache:

    # Saves access token to JSON file (expires_at as timestamp).

    def __init__(self, cache_path: str = ".auth_token.json"):
        self.cache_file = Path(cache_path)

    def save(self, token: str, expires_at: float):
        data = {"access_token": token, "expires_at": expires_at}
        self.cache_file.write_text(json.dumps(data), encoding="utf-8")

    def load(self) -> Tuple[Optional[str], float]:
        if not self.cache_file.exists():
            return None, 0.0
        try:
            data = json.loads(self.cache_file.read_text(encoding="utf-8"))
            return data.get("access_token"), float(data.get("expires_at", 0.0))
        except (json.JSONDecodeError, ValueError):
            return None, 0.0
