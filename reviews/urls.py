from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ReviewsListView.as_view(), name="list"),
    url(r'^add$', views.AgencyReviewCreateView.as_view(), name="create"),
    url(r'^(?P<pk>\d{1,}?)$', views.AgencyReviewDetailView.as_view(), name="detail"),
    url(r'^(?P<review_id>\d{1,}?)/vote/(?P<vote>(up|down))$', views.AgencyReviewVoteView.as_view(), name="vote"),
)
