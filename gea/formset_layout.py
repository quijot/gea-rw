from crispy_forms.layout import TEMPLATE_PACK, LayoutObject
from django.template.loader import render_to_string


class Formset(LayoutObject):
    template = "bootstrap4/table_inline_formset.html"

    def __init__(self, formset_name_in_context, template=None, helper=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        self.helper = helper  # helper don't work with InlineFormset
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(
            self.template,
            {
                "formset": formset,
                "form_id": self.formset_name_in_context,
                "helper": self.helper,
            },
        )
