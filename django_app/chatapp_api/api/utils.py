import functools
import logging

from .exceptions import AuthorizationError


def try_request_with_token_auth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            if self._token_repository.token_exist():
                pair_tokens = self._token_repository.get_tokens()
                access_token = pair_tokens.access_token
                refresh_token = pair_tokens.refresh_token
            else:
                pair_tokens = self.auth()
                access_token = pair_tokens.access_token
                refresh_token = pair_tokens.refresh_token
            return method(
                self, *args,
                access_token=access_token,
                refresh_token=refresh_token,
                **kwargs
            )
        except AuthorizationError as e:
            logging.info(f'Auth err: {e}')
            pair_tokens = self.auth()
            access_token = pair_tokens.access_token
            refresh_token = pair_tokens.refresh_token
            return method(
                self, *args,
                access_token=access_token,
                refresh_token=refresh_token,
                **kwargs
            )
    return wrapper
