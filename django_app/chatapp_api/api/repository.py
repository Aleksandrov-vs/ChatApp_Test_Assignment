from datetime import datetime

from chatapp_api.api.models import AuthResponse, PairOfTokens
from chatapp_api.models import Token
from django.utils import timezone


class TokenRepository:
    @staticmethod
    def get_tokens() -> PairOfTokens | None:
        token = Token.objects.first()
        if token is None:
            return None
        return PairOfTokens(
            access_token=token.access_token,
            refresh_token=token.refresh_token
        )

    @staticmethod
    def token_exist() -> bool:
        token = Token.objects.first()
        if token is None:
            return False
        return True

    @staticmethod
    def update_token(auth_response: AuthResponse) -> PairOfTokens:
        token = Token.objects.first()
        if token is None:
            token = Token()
        token.refresh_token = auth_response.refreshToken
        token.refresh_expired_date = datetime.fromtimestamp(
            auth_response.refreshTokenEndTime,
            tz=timezone.utc
        )
        token.access_token = auth_response.accessToken
        token.access_expired_date = datetime.fromtimestamp(
            auth_response.accessTokenEndTime,
            tz=timezone.utc
        )
        token.save()
        return PairOfTokens(
            access_token=auth_response.accessToken,
            refresh_token=auth_response.refreshToken
        )
