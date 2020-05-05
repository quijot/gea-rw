from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

from gea.views import Home

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("gea/", include("gea.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("", Home.as_view(), name="home"),
    path("nested_admin/", include("nested_admin.urls")),
]
