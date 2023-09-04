from functools import wraps

from django.http import Http404

from phone_notifications.models import Mailing


def user_has_mailing_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        try:
            pk = kwargs['pk']
            script = Mailing.objects.get(pk=pk)
            if script.user != user:
                raise Http404("You don't have access to this page.")

        except Mailing.DoesNotExist:
            raise Http404("You don't have access to this page.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
