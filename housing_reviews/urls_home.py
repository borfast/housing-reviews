from django.conf.urls import patterns, url
# from django.views.generic.base import TemplateView,
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    '',
    # url(r'^$', TemplateView.as_view(template_name="housing_reviews/home.html"), name="home"),
    url(r'^$', RedirectView.as_view(url='/reviews'), name="home"),
)
