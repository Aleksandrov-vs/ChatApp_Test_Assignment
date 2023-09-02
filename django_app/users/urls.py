from users.views import SingUpView
from django.urls import path

urlpatterns = [
    path("sign-up/", SingUpView.as_view(), name="sign-up"),
]