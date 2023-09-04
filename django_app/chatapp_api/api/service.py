import logging
from http import HTTPStatus

import requests
from chatapp_api.api.models import (AuthResponse, CheckPhoneResponse,
                                    PairOfTokens, SendMsgResponse)
from chatapp_api.api.repository import TokenRepository
from chatapp_api.api.utils import try_request_with_token_auth

from .exceptions import AuthorizationError, PhoneDoesNotExist


class ChatAppApiService:
    def __init__(
            self,
            user_email: str,
            user_password: str,
            app_id: str,
            license_id: str,
            token_repository: TokenRepository
    ):
        self._base_url = 'https://api.chatapp.online'
        self._user_email = user_email
        self._user_password = user_password
        self._app_id = app_id
        self._token_repository = token_repository
        self._license_id = license_id

        if self._token_repository.get_tokens() is None:
            self.auth()

    def auth(self) -> PairOfTokens:
        auth_url = self._base_url + '/v1/tokens'
        payload = {
            "email": self._user_email,
            "password": self._user_password,
            "appId":  self._app_id
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            'POST', auth_url,
            headers=headers,
            json=payload
        )
        if response.status_code != HTTPStatus.OK:
            raise AuthorizationError('Authentication error')

        data = response.json()
        auth_response = AuthResponse(**data['data'])
        return self._token_repository.update_token(auth_response)

    @try_request_with_token_auth
    def refresh_token(self, **kwargs):
        refresh_url = self._base_url + '/v1/tokens/refresh'
        refresh_token = kwargs.get('refresh_token')

        headers = {
            'Refresh':  refresh_token
        }

        response = requests.request('POST', refresh_url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            logging.info('Authentication error')
            return None
        data = response.json()
        auth_response = AuthResponse(**data['data'])
        self._token_repository.update_token(auth_response)

    @try_request_with_token_auth
    def check_phone(self, phone_number: str, **kwargs) -> bool:
        url = self._base_url + f'/v1/licenses/{self._license_id}/messengers/' \
                               f'grWhatsApp/phones/{phone_number}/check'
        access_token = kwargs.get('access_token')
        headers = {
            'Authorization': access_token
        }

        response = requests.request('GET', url, headers=headers)
        if response.status_code == HTTPStatus.FORBIDDEN:
            raise AuthorizationError
        if response.status_code != HTTPStatus.OK:
            return False
        else:
            data = response.json()
            check_phone = CheckPhoneResponse(**data['data'])
            return check_phone.exist

    @try_request_with_token_auth
    def send_text_message(
            self,
            phone_number: str,
            msg_text: str,
            **kwargs
    ) -> SendMsgResponse:
        url = self._base_url + f'/v1/licenses/' \
                               f'{self._license_id}/messengers/grWhatsApp/' \
                               f'chats/{phone_number}/messages/text'
        payload = {
            "text": msg_text,
        }
        access_token = kwargs.get('access_token')

        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
        if not self.check_phone(phone_number):
            raise PhoneDoesNotExist()

        response = requests.request('POST', url, headers=headers, json=payload)
        return SendMsgResponse(**response.json())
