import logging
from uuid import UUID

from chatapp_api.api.exceptions import AuthorizationError, PhoneDoesNotExist
from chatapp_api.api.repository import TokenRepository
from chatapp_api.api.service import ChatAppApiService
from config.celery import app
from django.conf import settings

from .models import PhoneNotification, SendStatus


@app.task
def send_message(phone_notif_id: UUID, msg_text: str):
    phone_notif = PhoneNotification.objects.get(pk=phone_notif_id)
    chat_app_service = ChatAppApiService(
        user_email=settings.CHAT_API_SETTINGS.user_email,
        user_password=settings.CHAT_API_SETTINGS.user_password,
        app_id=settings.CHAT_API_SETTINGS.app_id,
        license_id=settings.CHAT_API_SETTINGS.license_id,
        token_repository=TokenRepository()
    )
    logging.info(f'Отправка сообщения: {phone_notif.number}')
    try:
        send_msg_response = chat_app_service.send_text_message(
            phone_notif.number,
            msg_text
        )
    except AuthorizationError as e:
        phone_notif.send_status = SendStatus.ERR
        phone_notif.err_text = 'ошибка в работе сервиса, попробуйте позже(('
        phone_notif.save()

        return f"Auth err: {e}"
    except PhoneDoesNotExist:
        phone_notif.send_status = SendStatus.ERR
        phone_notif.err_text = 'Такого пользователя нет.'
        phone_notif.save()
        return f"Phone number {phone_notif.number} does not exist."

    if not send_msg_response.success:
        phone_notif.send_status = SendStatus.ERR
        phone_notif.save()
        return "неизвестная ошибка"
    phone_notif.send_status = SendStatus.SENT
    phone_notif.save()
    return f"Message send to {phone_notif.number}."
