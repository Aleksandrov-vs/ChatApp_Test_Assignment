from django.urls import path
from phone_notifications.views import MailingDetailView, MailingView

urlpatterns = [
    path('', MailingView.as_view(), name='home'),
    path(
        'mailing/<uuid:pk>/',
        MailingDetailView.as_view(),
        name='mailing_detail'
    ),
]
