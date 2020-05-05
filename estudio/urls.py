from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from gea.views import Home

urlpatterns = [
    path("accounts/login/", auth_views.login, name="login"),
    path("admin/", admin.site.urls),
    path("gea/", include("gea.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("", Home.as_view(), name="home"),
    path("nested_admin/", include("nested_admin.urls")),
]
