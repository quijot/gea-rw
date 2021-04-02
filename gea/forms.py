from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Fieldset, Layout, Row, Submit
from django import forms
from django.urls import reverse_lazy

from . import gea_vars as gv
from . import models
from .formset_layout import Formset


class PersonasForm(forms.ModelForm):
    class Meta:
        model = models.ExpedientePersona
        fields = "__all__"


PersonasInlineFormSet = forms.inlineformset_factory(
    models.Expediente,
    models.ExpedientePersona,
    form=PersonasForm,
    fields="__all__",
    extra=1,
)


LugaresInlineFormSet = forms.inlineformset_factory(
    models.Expediente,
    models.ExpedienteLugar,
    fields=(
        "id",
        "lugar",
    ),
    extra=1,
)


class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = models.Expediente
        fields = [
            "id",
            "inscripcion_numero",
            "duplicado",
            "sin_inscripcion",
            "orden_numero",
            "cancelado",
            "cancelado_por",
            "objetos",
            "profesionales_firmantes",
            "fecha_medicion",
            "inscripcion_fecha",
            "orden_fecha",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Div("id", css_class="col-md-2"),
                    Div(Field("fecha_medicion", css_class="date", id="datepicker"), css_class="col-md-2"),
                    Div("inscripcion_numero", css_class="col-md-2"),
                    Div(Field("inscripcion_fecha", css_class="date", id="datepicker"), css_class="col-md-2"),
                    Div("duplicado", css_class="col-md-2"),
                    Div("sin_inscripcion", css_class="col-md-2"),
                    Div("orden_numero", css_class="col-md-2"),
                    Div(Field("orden_fecha", css_class="date", id="datepicker"), css_class="col-md-2"),
                    Div("cancelado", css_class="col-md-2"),
                    Div("cancelado_por", css_class="col-md-2"),
                    Div("objetos", css_class="col-md-6"),
                    Div("profesionales_firmantes", css_class="col-md-6"),
                ),
            ),
            Fieldset(
                "Lugares",
                Button(
                    "add-lugar",
                    "&plus; Lugar",
                    css_class="btn-sm btn-primary",
                    title="Agregar otro Lugar",
                    onclick="add_form('lugares')",
                ),
                Formset("lugares"),
            ),
            Fieldset(
                "Personas involucradas",
                Button(
                    "add-persona",
                    "&plus; Persona",
                    css_class="btn-sm btn-primary",
                    title="Agregar otra Persona",
                    onclick="add_form('personas')",
                ),
                Formset("personas"),
            ),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-secondary",
                    onclick=f"window.location.href = '{reverse_lazy('personas')}';",
                ),
                Submit("save", "Guardar"),
                style="text-align: right;",
            ),
        )


class PersonaForm(forms.ModelForm):
    class Meta:
        model = models.Persona
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Datos personales",
                Row(
                    Div("apellidos", css_class="col-lg-6"),
                    Div("nombres", css_class="col-lg-6"),
                ),
                Row(
                    Div("apellidos_alternativos", css_class="col-lg-6"),
                    Div("nombres_alternativos", css_class="col-lg-6"),
                ),
                Row(
                    Div("tipo_doc", css_class="col-lg-4"),
                    Div("documento", css_class="col-lg-4"),
                    Div("cuit_cuil", css_class="col-lg-4"),
                ),
            ),
            Fieldset(
                "Contacto",
                Row(
                    Div("domicilio", css_class="col-lg-8"),
                    Div("lugar", css_class="col-lg-4"),
                    Div("telefono", css_class="col-lg-6"),
                    Div("email", css_class="col-lg-6"),
                ),
            ),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-secondary",
                    onclick=f"window.location.href = '{reverse_lazy('personas')}';",
                ),
                Submit("save", "Guardar"),
                style="text-align: right;",
            ),
        )


class CaratulaForm(forms.Form):
    expte_nro = forms.IntegerField(label="Expediente", widget=forms.NumberInput(attrs={"placeholder": "ej: 4300"}))
    inmueble = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "ej: Una fracción de terreno..."}), required=False
    )
    matricula = forms.IntegerField(required=False)
    tomo = forms.IntegerField(required=False)
    par = forms.BooleanField(required=False)
    folio = forms.IntegerField(required=False)
    numero = forms.IntegerField(label="Número", required=False)
    fecha = forms.DateField(required=False)
    obs = forms.CharField(
        label="Observaciones generales",
        widget=forms.Textarea(attrs={"placeholder": "ej: Modifica el Lote 1 del Plano 23.456."}),
        required=False,
    )
    obs_esp = forms.CharField(label="Observaciones específicas", widget=forms.Textarea(), required=False)
    FORMAT_CHOICES = (
        ("html", "HTML"),
        ("dxf", "DXF"),
    )
    fmt = forms.ChoiceField(label="Formato de salida", choices=FORMAT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div("expte_nro", css_class="col-md-3"),
                Div("fmt", css_class="col-md-3"),
                Div(
                    FormActions(
                        Button(
                            "cancel",
                            "Cancelar",
                            css_class="btn-secondary",
                            onclick=f"window.location.href = '{reverse_lazy('expedientes')}';",
                        ),
                        Submit("save", "Generar"),
                        style="text-align: right;",
                    ),
                    css_class="col-md-6",
                ),
            ),
            Div("inmueble"),
            Fieldset(
                "DOMINIO",
                Row(
                    Div("matricula", css_class="col-md-2"),
                    Div(css_class="col"),
                    Div("tomo", css_class="col-md-2"),
                    Div("par", css_class="col-md-1"),
                    Div("folio", css_class="col-md-2"),
                    Div("numero", css_class="col-md-2"),
                    Div(Field("fecha", css_class="date", id="datepicker"), css_class="col-md-2"),
                ),
            ),
            Fieldset(
                "OBSERVACIONES",
                Div("obs"),
                Div("obs_esp"),
            ),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-secondary",
                    onclick=f"window.location.href = '{reverse_lazy('expedientes')}';",
                ),
                Submit("save", "Generar"),
                style="text-align: right;",
            ),
        )


class SolicitudForm(forms.Form):
    expte_nro = forms.IntegerField(
        label="Expediente",
        widget=forms.NumberInput(attrs={"placeholder": "ej: 4300"}),
    )
    circunscripcion = forms.ChoiceField(label="Circunscripción", choices=gv.CIRC, initial=gv.CIRC_DEFAULT)
    domicilio_fiscal = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={"placeholder": "ej: San Martín 430"}),
    )
    localidad = forms.ChoiceField(choices=gv.CP, initial=gv.CP_DEFAULT)
    provincia = forms.ChoiceField(choices=gv.PROV, initial=gv.PROV_DEFAULT)
    nota_titulo = forms.ChoiceField(label="Nota título", choices=gv.NOTA)
    nota = forms.CharField(
        label="Nota contenido",
        widget=forms.Textarea(attrs={"placeholder": "Ingrese el texto de la nota correspondiente"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div("expte_nro", css_class="col-lg-4"),
                Div("circunscripcion", css_class="col-lg-8"),
            ),
            Div("domicilio_fiscal"),
            Row(Div("localidad", css_class="col-lg-6"), Div("provincia", css_class="col-lg-6")),
            Div("nota_titulo"),
            Div("nota"),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-dark",
                    onclick=f"window.location.href = '{reverse_lazy('home')}';",
                ),
                Submit("save", "Generar Nota"),
                css_class="float-right",
            ),
        )


class VisacionForm(forms.Form):
    expte_nro = forms.IntegerField(
        label="Expediente",
        widget=forms.NumberInput(attrs={"placeholder": "ej: 4300"}),
    )
    lugar = forms.ChoiceField(choices=gv.LUGAR, initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div("expte_nro"),
            Div("lugar"),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-dark",
                    onclick=f"window.location.href = '{reverse_lazy('home')}';",
                ),
                Submit("save", "Generar Nota"),
                css_class="float-right",
            ),
        )


#
# Buscar Plano por Nro
#
class PlanoForm(forms.Form):
    circ = forms.IntegerField(label="Circunscripción", min_value=1, max_value=2, initial=1)
    n_insc = forms.IntegerField(label="Plano Nº", min_value=1, max_value=999999)


#
# Buscar Set de Datos por PII
#
class SetForm(forms.Form):
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(label="Subpartida", min_value=0, max_value=9999, initial=0)


#
# Calcular Digito Verificador de la PII
#
class DVAPIForm(forms.Form):
    dp = forms.IntegerField(label="DP (departamento)", min_value=1, max_value=19, initial=11)
    ds = forms.IntegerField(label="DS (distrito)", min_value=1, max_value=99, initial=8)
    sd = forms.IntegerField(label="SD (subdistrito)", min_value=0, max_value=99, initial=0)
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(label="Subpartida", min_value=0, max_value=9999, initial=0)


#
# Consultar estado en Sistema de Información de Expedientes del SCIT
#
class SIEForm(forms.Form):
    mesa = forms.IntegerField(min_value=13401, max_value=13401, initial=13401)
    nro = forms.IntegerField(label="Número", min_value=1, max_value=9999999)
    digito = forms.IntegerField(label="Dígito", min_value=0, max_value=9, initial=0)


#
#
# Exptes x Catastro Local
#
#
class CLForm(forms.Form):
    lugar = forms.ModelChoiceField(
        queryset=models.Lugar.objects.exclude(nombre__startswith="Colonia")
        .exclude(nombre__startswith="Zona Rural")
        .exclude(nombre__startswith="Zona de Islas"),
        required=False,
    )
    seccion = forms.CharField(max_length=4, required=False)
    manzana = forms.CharField(max_length=4, required=False)
    parcela = forms.CharField(max_length=4, required=False)
