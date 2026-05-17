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
