import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.conf import settings

from phone_notifications.decorators.access_decorators import \
    user_has_mailing_access
from phone_notifications.forms import MailingForm, PhoneNumberFormSet
from phone_notifications.models import Mailing

from .tasks import send_message


@method_decorator(login_required(), name='dispatch')
class MailingView(ListView):
    template_name = 'home.html'
    model = Mailing
    context_object_name = 'mailing_list'
    success_url = 'home'

    def get_queryset(self):
        current_user = self.request.user
        return Mailing.objects.filter(
            user=current_user
        ).order_by('-modified')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm()
        context['phone_number_formset'] = PhoneNumberFormSet()
        return context

    def post(self, request, *args, **kwargs):
        mailing_form = MailingForm(request.POST)

        if not mailing_form.is_valid():
            return render(request, self.template_name, {
                'mailing_form': mailing_form,
                'phone_number_formset': PhoneNumberFormSet(request.POST),
                self.context_object_name: self.get_queryset()
            })

        mailing = mailing_form.save(commit=False)
        mailing.user = request.user
        phone_number_formset = PhoneNumberFormSet(
            request.POST,
            instance=mailing
        )

        if not phone_number_formset.is_valid():
            return render(request, self.template_name, {
                'mailing_form': mailing_form,
                'phone_number_formset': phone_number_formset,
                self.context_object_name: self.get_queryset()
            })

        mailing.save()
        phone_number_set = phone_number_formset.save()

        for phone_number in phone_number_set:
            delay_seconds = random.randint(
                settings.CHAT_API_SETTINGS.lower_limit_delay,
                settings.CHAT_API_SETTINGS.upper_limit_delay
            )
            send_message.apply_async(
                [phone_number.id, mailing.message],
                countdown=delay_seconds
            )

        return HttpResponseRedirect(reverse(self.success_url))


@method_decorator([login_required(), user_has_mailing_access], name='dispatch')
class MailingDetailView(DetailView):
    template_name = 'mailing_detail.html'
    model = Mailing
    context_object_name = 'mailing'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        mailing_with_phone_notifications = Mailing.objects.filter(
            pk=pk
        ).prefetch_related('phone_notification').order_by('-modified')
        return mailing_with_phone_notifications
