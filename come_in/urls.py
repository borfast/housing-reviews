from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from .views import CreateInvitationKeyView, InvitationAccepted

urlpatterns = patterns('',
    # url(r'^invite/$', invite, name='invitation_invite'),
    url(r'^invite$', CreateInvitationKeyView.as_view(), name='invitation_invite'),

    url(r'^invite/complete$',
                TemplateView.as_view(template_name='come_in/invitation_complete.html'),
                name='invitation_complete'),

    url(r'^accept/(?P<invitation_key>\w+)/$', InvitationAccepted.as_view(), name='invitation_invited'),

    # url(r'^register/$',
    #             register,
    #             { 'backend': 'registration.backends.default.DefaultBackend' },
    #             name='registration_register'),
)