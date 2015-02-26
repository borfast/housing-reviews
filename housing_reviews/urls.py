from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf import settings
from django.views.generic import TemplateView

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'^', include('subscribe.urls', namespace="subscribe")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^invitations/', include('come_in.urls')),

    url(r'^home/$', include('housing_reviews.urls_home', namespace="home")),
    url(r'^about/$', TemplateView.as_view(template_name="housing_reviews/about.html"), name='about'),
    url(r'^agencies/', include('agencies.urls', namespace="agencies")),
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),


    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^mightyadmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^mightyadmin/', include(admin.site.urls)),
)

# if getattr(settings, 'DEBUG', False):
#     urlpatterns += staticfiles_urlpatterns()

# if not getattr(settings, 'DEBUG', False):
#     urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
#     print
#     urlpatterns += patterns(
#         '',
#         (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )
