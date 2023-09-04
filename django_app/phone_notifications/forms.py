from django import forms

from phone_notifications.models import Mailing, PhoneNotification


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message']


class PhoneNotificationForm(forms.ModelForm):
    class Meta:
        model = PhoneNotification
        fields = ['number']


PhoneNumberFormSet = forms.inlineformset_factory(
    Mailing,
    PhoneNotification,
    form=PhoneNotificationForm,
    extra=1,
    can_delete=False,
)
