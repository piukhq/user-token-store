from typing import Any, Dict, List, Optional

import requests

from redis import StrictRedis


class UserTokenStore:
    class NoSuchToken(Exception):
        pass

    class TokenError(Exception):
        pass

    def __init__(self, redis_url: str) -> None:
        """
        Create a token store.
        """
        self.storage = StrictRedis.from_url(redis_url)

    @staticmethod
    def _key(scheme_account_id: str) -> str:
        """
        Creates a key for the given scheme account.

        :param scheme_account_id: The scheme account ID to create the key for.
        :return: A string key to use as the key for the given scheme account ID.
        """
        return f"user-token-scheme-account-{scheme_account_id}"

    def get(self, scheme_account_id: str) -> str:
        """
        Find an auth token for the given scheme account. Raises an AuthTokenStore.NoSuchToken exception on failure.

        :param scheme_account_id: The scheme account ID to search for.
        :raises UserTokenStore.NoSuchToken: When token does not exist
        :return: The auth token.
        """
        token = self.storage.get(self._key(scheme_account_id))
        if not token:
            raise self.NoSuchToken(f"There is no token stored for scheme_account_id `{scheme_account_id}`")
        return token.decode()

    def set(self, scheme_account_id: str, token: str) -> None:
        """
        Set an auth token for a given scheme account.

        :param scheme_account_id: The scheme account ID to associate with the token.
        :param token: The auth token to save.
        :return: None
        """
        self.storage.set(self._key(scheme_account_id), token)

    def delete(self, scheme_account_id: str) -> None:
        """
        Delete an auth token for the given scheme account.

        :param scheme_account_id: The scheme account ID to search for.
        :return: None
        """
        self.storage.delete(self._key(scheme_account_id))

    def get_new(
        self,
        url: str,
        token_path: List[str],
        scheme_account_id: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Any] = None,
    ) -> str:
        """
        Generic API call to get new user tokens. If you can't use this, set user token in Midas agent and call it.

        :param url: URL to call to get auth token.
        :param token_path: a list of JSON keys required to get to user token in a nested JSON response
            (still use a single value list for flat JSON) e.g. [CustomerSignOnResult, token]
        :param scheme_account_id: The scheme account ID to associate with the token.
        :param method: HTTP request method to get auth token.
        :param headers: Headers to send in the request.
        :param data: dict to send as form data in the request.
        :param json: dict to send as json in the request.
        :param params: dict to be sent as the query string in the request.
        :raises UserTokenStore.TokenError: When when there was an error extracting the token from the response payload
        :return: The new auth token.
        """
        try:
            response = requests.request(method, url, headers=headers, data=data, json=json, params=params)
            response_json = response.json()

            for key in token_path:
                response_json = response_json[key]

            user_token = response_json
            self.storage.set(self._key(scheme_account_id), user_token)
            return user_token

        except (ValueError, KeyError) as e:
            raise self.TokenError(f"There was an error getting user token from request: {e}") from e
