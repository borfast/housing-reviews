from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.SubscribeView.as_view(), name="home"),
    url(r'^confirm/$', TemplateView.as_view(template_name="subscribe/confirm.html"), name="confirm"),
    url(r'^thanks/$', TemplateView.as_view(template_name="subscribe/thanks.html"), name="thanks"),
)
