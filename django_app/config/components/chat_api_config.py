from pydantic import Field
from pydantic_settings import BaseSettings


class ChatApiSettings(BaseSettings):
    user_email: str = Field(env='USER_EMAIL')
    user_password: str = Field(env='USER_PASSWORD')
    app_id: str = Field(env='APP_ID')
    license_id: int = Field(env='LICENSE_ID')

    lower_limit_delay: int = Field(5, env='LOWER_LIMIT_DELAY')
    upper_limit_delay: int = Field(5, env='UPPER_LIMIT_DELAY')


CHAT_API_SETTINGS = ChatApiSettings()
