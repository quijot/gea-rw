from django.conf.urls import include, url
from django.contrib import admin

from gea.views import Home
from filebrowser.sites import site

from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^accounts/login/$', auth_views.login),
    url(r'^admin/', admin.site.urls),
    url(r'^gea/', include('gea.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^nested_admin/', include('nested_admin.urls')),
]


from django.conf import settings


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns = urlpatterns + [
        url(r'^(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),
    ]

