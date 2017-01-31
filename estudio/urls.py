from django.conf.urls import include, url
from django.contrib import admin

from gea.views import Home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^gea/', include('gea.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', Home.as_view(), name='home'),
]

#try:
#    import grappelli
#    urlpatterns = urlpatterns + [
#        url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
#    ]
#except ImportError, e:
#    if e.message != 'No module named grappelli':
#        raise
urlpatterns = urlpatterns + [
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
]

#try:
#    import nested_admin
#    urlpatterns = urlpatterns + [
#        url(r'^nested_admin/', include('nested_admin.urls')),
#    ]
#except ImportError, e:
#    if e.message != 'No module named nested_admin':
#        raise
urlpatterns = urlpatterns + [
    url(r'^nested_admin/', include('nested_admin.urls')),
]

#from estudio import settings

#urlpatterns = urlpatterns + [
#    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT,
#        }),
#]

from django.conf import settings

# ... your normal urlpatterns here

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns = urlpatterns + [
        url(r'^(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),
    ]

