from django.conf.urls import patterns, url

from . import views
from reviews import views as review_views

urlpatterns = patterns(
    '',
    url(r'^$', views.AgenciesListView.as_view(), name="list"),
    url(r'^(?P<pk>\d{1,}?)$', views.AgencyDetailView.as_view(), name="detail"),
    url(r'^(?P<agency_id>\d{1,}?)/reviews$', review_views.ReviewsListView.as_view(), name="reviews_list"),
)
