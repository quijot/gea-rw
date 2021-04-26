from django.urls import path

from . import views

urlpatterns = [
    # Inicio
    path("", views.Home.as_view(), name="home"),
    # About
    path("acerca/", views.About.as_view(), name="about"),
    # Catastros Locales
    path("catastros-locales/", views.CatastroLocalListView.as_view(), name="catastros_locales"),
    # Expedientes
    path("expedientes/", views.ExpedienteListView.as_view(), name="expedientes"),
    path("expediente/<int:pk>/", views.ExpedienteDetailView.as_view(), name="expediente"),
    path("expediente/crear/", views.ExpedienteCreateView.as_view(), name="expediente_create"),
    path("expediente/editar/<int:pk>/", views.ExpedienteUpdateView.as_view(), name="expediente_update"),
    path("expediente/borrar/<int:pk>/", views.ExpedienteDeleteView.as_view(), name="expediente_delete"),
    path(
        "expedientepersona/borrar/<int:pk>/",
        views.ExpedientePersonaDeleteView.as_view(),
        name="expedientepersona_delete",
    ),
    # ExpedienteLugar
    path("expedientelugar/crear/", views.ExpedienteLugarCreateView.as_view(), name="expedientelugar_create"),
    path("expedientelugar/editar/<int:pk>/", views.ExpedienteLugarUpdateView.as_view(), name="expedientelugar_update"),
    path("expedientelugar/borrar/<int:pk>/", views.ExpedienteLugarDeleteView.as_view(), name="expedientelugar_delete"),
    # ExpedientePartida
    path("expediente/<int:expediente_id>/partidas/", views.add_partida_to_expediente, name="partida_to_expediente"),
    path(
        "expediente/<int:expediente_id>/partidas/<int:partida_id>/",
        views.update_partida_to_expediente,
        name="partida_to_expediente",
    ),
    path(
        "expediente/partidas/<int:pk>/borrar/",
        views.ExpedientePartidaDeleteView.as_view(),
        name="expedientepartida_delete",
    ),
    # Personas
    path("personas/", views.PersonaListView.as_view(), name="personas"),
    path("persona/<int:pk>/", views.PersonaDetailView.as_view(), name="persona"),
    path("persona/crear/", views.PersonaCreateView.as_view(), name="persona_create"),
    path("persona/editar/<int:pk>/", views.PersonaUpdateView.as_view(), name="persona_update"),
    path("persona/borrar/<int:pk>/", views.PersonaDeleteView.as_view(), name="persona_delete"),
    # Notas
    path("solicitud/", views.solicitud, name="solicitud"),
    path("solicitud/<int:expediente>/", views.solicitud, name="solicitud"),
    path("visacion/", views.visacion, name="visacion"),
    path("visacion/<int:expediente>/", views.visacion, name="visacion"),
    # Búsquedas
    path("plano/", views.plano, name="buscar_plano"),
    path("set/", views.set, name="buscar_set"),
    path("catastro/", views.catastro, name="buscar_catastro"),
    # Herramientas
    path("caratula/", views.caratula, name="caratula"),
    path("caratula/<int:expediente>/", views.caratula, name="caratula"),
    path("dvapi/", views.dvapi, name="dvapi"),
    path("sie/", views.sie, name="sie"),
]
