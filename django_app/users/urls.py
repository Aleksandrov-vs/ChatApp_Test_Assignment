from django.urls import path
from users.views import SingUpView

urlpatterns = [
    path("sign-up/", SingUpView.as_view(), name="sign-up"),
]
