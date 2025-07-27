import json
import pytest
from pathlib import Path
from offers_sdk.token_cache import TokenCache


def test_load_returns_none_on_jsondecodeerror(tmp_path):
    cache_file = tmp_path / ".auth_token.json"
    cache_file.write_text("not valid json", encoding="utf-8")

    token_cache = TokenCache(cache_path=str(cache_file))
    token, expires = token_cache.load()

    assert token is None
    assert expires == 0.0


def test_load_returns_none_on_valueerror(tmp_path):
    cache_file = tmp_path / ".auth_token.json"
    broken_data = {"access_token": "fake-token", "expires_at": "not-a-float"}
    cache_file.write_text(json.dumps(broken_data), encoding="utf-8")

    token_cache = TokenCache(cache_path=str(cache_file))
    token, expires = token_cache.load()

    assert token is None
    assert expires == 0.0
