from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain')),

    url(r'^$', RedirectView.as_view(url='/reviews'), name="home"),
    url(r'^home/$', RedirectView.as_view(url='/reviews')),
    url(r'^reviews/', include('reviews.urls', namespace="reviews")),
    url(r'^agencies/', include('agencies.urls', namespace="agencies")),
    url(r'^about/$', TemplateView.as_view(
        template_name="housing_reviews/about.html"), name='about'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^mightyadmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^mightyadmin/', include(admin.site.urls)),
)

# if getattr(settings, 'DEBUG', False):
#     urlpatterns += staticfiles_urlpatterns()

if not getattr(settings, 'DEBUG', False):
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
