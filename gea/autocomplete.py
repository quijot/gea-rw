from django_tomselect.autocompletes import AutocompleteModelView

from . import models


class PersonaAutocomplete(AutocompleteModelView):
    model = models.Persona
    search_lookups = ["apellidos__icontains", "nombres__icontains"]
    value_fields = ["id", "apellidos", "nombres"]

    def hook_prepare_results(self, results):
        for r in results:
            r["nombre_completo"] = f"{r['apellidos']} {r['nombres']}".strip()
        return results


class LugarAutocomplete(AutocompleteModelView):
    model = models.Lugar
    search_lookups = ["nombre__icontains"]
    value_fields = ["id", "nombre"]


class ExpedienteAutocomplete(AutocompleteModelView):
    model = models.Expediente
    search_lookups = ["id__icontains"]
    value_fields = ["id"]


class ObjetoAutocomplete(AutocompleteModelView):
    model = models.Objeto
    search_lookups = ["nombre__icontains"]
    value_fields = ["id", "nombre"]


class SdAutocomplete(AutocompleteModelView):
    model = models.Sd
    search_lookups = []  # Custom multi-word AND search below
    value_fields = ["id", "sd", "nombre", "ds__dp__dp", "ds__ds"]

    def hook_queryset(self, queryset):
        from django.db.models import CharField, F, Value
        from django.db.models.functions import Cast, Concat, LPad

        return queryset.select_related("ds__dp").annotate(
            _completo=Concat(
                LPad(Cast(F("ds__dp__dp"), output_field=CharField()), 2, Value("0")),
                LPad(Cast(F("ds__ds"), output_field=CharField()), 2, Value("0")),
                LPad(Cast(F("sd"), output_field=CharField()), 2, Value("0")),
                output_field=CharField(),
            )
        )

    def search(self, queryset, query):
        from django.db.models import Q

        if not query:
            return queryset
        q = Q()
        for word in query.split():
            q &= (
                Q(nombre__icontains=word)
                | Q(ds__nombre__icontains=word)
                | Q(ds__dp__nombre__icontains=word)
                | Q(_completo__icontains=word)
            )
        return queryset.filter(q).distinct()

    def hook_prepare_results(self, results):
        for r in results:
            dp = str(r.get("ds__dp__dp") or "").zfill(2)
            ds = str(r.get("ds__ds") or "").zfill(2)
            sd = str(r.get("sd") or "").zfill(2)
            nombre = r.get("nombre") or ""
            r["label"] = f"{dp}-{ds}-{sd} {nombre}".strip()
        return results
