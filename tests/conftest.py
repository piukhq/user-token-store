import os
import uuid

from unittest.mock import MagicMock

import pytest
import redis
import requests

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


@pytest.fixture(scope="session")
def redis_url() -> str:
    return REDIS_URL


@pytest.fixture(scope="session")
def redis_client(redis_url) -> redis.StrictRedis:
    return redis.StrictRedis.from_url(redis_url)


@pytest.fixture(scope="function")
def random_key() -> str:
    return uuid.uuid4().hex


@pytest.fixture(scope="function")
def random_value() -> str:
    return uuid.uuid4().hex


@pytest.fixture(scope="function")
def patch_requests(monkeypatch) -> MagicMock:
    response_mock = MagicMock()

    def mock_request(*args, **kwargs):
        return response_mock

    monkeypatch.setattr(requests, "request", mock_request)

    return response_mock
