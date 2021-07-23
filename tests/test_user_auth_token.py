import pytest

from user_auth_token import UserTokenStore


def test_get_no_exist(redis_url, random_key) -> None:

    store = UserTokenStore(redis_url)

    with pytest.raises(store.NoSuchToken):
        store.get(random_key)


def test_set_get(redis_url, random_key, random_value) -> None:

    store = UserTokenStore(redis_url)

    store.set(random_key, random_value)
    new_value = store.get(random_key)

    assert random_value == new_value, "Token retrieved from redis is not what was stored"


def test_delete(redis_url, random_key, random_value) -> None:

    store = UserTokenStore(redis_url)

    store.set(random_key, random_value)
    new_value = store.get(random_key)
    assert random_value == new_value, "Token retrieved from redis is not what was stored"

    store.delete(random_key)

    with pytest.raises(store.NoSuchToken):
        store.get(random_key)


def test_get_new(redis_url, patch_requests, random_key, random_value) -> None:
    patch_requests.json.return_value = {"test1": random_value}

    store = UserTokenStore(redis_url)

    returned_token = store.get_new("https://yourmum.com", ["test1"], random_key)
    returned_token2 = store.get(random_key)

    assert returned_token == random_value, "Token retrieved from request is not correct"
    assert returned_token2 == random_value, "Token retrieved from redis is not what was stored"


def test_get_new_nested(redis_url, patch_requests, random_key, random_value) -> None:
    patch_requests.json.return_value = {"test1": {"test2": {"test3": random_value}}}

    store = UserTokenStore(redis_url)

    returned_token = store.get_new("https://yourmum.com", ["test1", "test2", "test3"], random_key)
    assert returned_token == random_value, "Token retrieved from request is not correct"


def test_get_bad_json_path(redis_url, patch_requests, random_key, random_value) -> None:
    patch_requests.json.return_value = {"test1": random_value}

    store = UserTokenStore(redis_url)

    with pytest.raises(store.TokenError):
        store.get_new("https://yourmum.com", ["nah_m8"], random_key)
