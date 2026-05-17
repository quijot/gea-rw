from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("gea/", include("gea.urls")),
    path("", RedirectView.as_view(url="gea/", permanent=True)),
    path("nested_admin/", include("nested_admin.urls")),
]

# Developing
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [path("accounts/", include("django.contrib.auth.urls"))]
