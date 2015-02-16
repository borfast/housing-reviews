# coding=utf-8
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from .forms import InterestedForm


class SubscribeView(CreateView):
    template_name = 'subscribe/subscribe_form.html'
    form_class = InterestedForm
    success_url = 'confirm'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/reviews')
        else:
            return super(SubscribeView, self).dispatch(request, args, kwargs)

    def form_valid(self, form):
        form.subscribe()
        #form.send_emails()
        return super(SubscribeView, self).form_valid(form)
