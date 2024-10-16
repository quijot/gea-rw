from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel


def capitalize_phrase(string):
    phrase = ""
    for word in string.split():
        phrase = f"{phrase} {word[0].upper()}{word[1:].lower()}"
    return phrase.strip()


class Antecedente(models.Model):
    expediente = models.ForeignKey("Expediente", on_delete=models.CASCADE)
    expediente_modificado = models.ForeignKey(
        "Expediente", blank=True, null=True, on_delete=models.CASCADE, related_name="expediente_modificado"
    )
    inscripcion_numero = models.IntegerField()
    duplicado = models.BooleanField(default=False)
    observacion = models.CharField(max_length=255, blank=True)
    plano_ruta = models.URLField(max_length=100, blank=True)
    # plano = FileBrowseField(
    #     "Enlace al plano", max_length=200, directory="planos/", extensions=[".pdf"],
    # )


class Catastro(models.Model):
    expediente_partida = models.ForeignKey("ExpedientePartida", on_delete=models.CASCADE)
    zona = models.ForeignKey("Zona", on_delete=models.CASCADE)
    seccion = models.CharField("sección", max_length=10, blank=True)
    poligono = models.CharField("polígono", max_length=10, blank=True)
    manzana = models.CharField(max_length=10, blank=True)
    parcela = models.CharField(max_length=10)
    subparcela = models.CharField(max_length=10, blank=True)

    def __str__(self):
        if self.zona.id in (1, 2, 3):
            return f"Z:{self.zona} - S:{self.seccion} - M:{self.manzana} - P:{self.parcela}"
        elif self.zona.id in (4, 5):
            return f"Z:{self.zona} - Pol:{self.poligono} - P:{self.parcela}"
        else:
            return ""


class CatastroLocal(models.Model):
    expediente_lugar = models.ForeignKey("ExpedienteLugar", on_delete=models.CASCADE)
    seccion = models.CharField("sección", max_length=20, blank=True)
    manzana = models.CharField(max_length=20, blank=True)
    parcela = models.CharField(max_length=20, blank=True)
    subparcela = models.CharField(max_length=20, blank=True)
    suburbana = models.BooleanField(default=False)
    poligono = models.CharField("polígono", max_length=20, blank=True)

    class Meta:
        verbose_name = "catastro local"
        verbose_name_plural = "catastros locales"

    def __str__(self):
        s = f"S:{self.seccion}" if self.seccion else ""
        m = f"M:{self.manzana}" if self.manzana else ""
        p = f"P:{self.parcela}" if self.parcela else ""
        return f"{s} {m} {p}".strip()


class Circunscripcion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=10)
    orden = models.CharField(max_length=7)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "circunscripciones"

    def __str__(self):
        return self.nombre


class Comprobante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Presupuesto(models.Model):
    expediente = models.ForeignKey("Expediente", on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()
    porcentaje_cancelado = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="% cancelado")
    observacion = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["expediente"]

    def __str__(self):
        return f"{self.expediente} - ${self.monto:.2f} - {self.fecha}"


class Pago(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT)
    comprobante = models.ForeignKey(Comprobante, on_delete=models.PROTECT)
    comprobante_nro = models.IntegerField()
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    observacion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.porcentaje}% - {self.fecha}"


class Dp(models.Model):
    dp = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="nombre depto")
    habitantes = models.IntegerField(blank=True)
    superficie = models.IntegerField(blank=True)
    cabecera = models.CharField(max_length=50, blank=True)
    circunscripcion = models.ForeignKey(Circunscripcion, on_delete=models.PROTECT)

    def departamento(self):
        return f"{self.dp:02d} {self.nombre}"

    class Meta:
        verbose_name_plural = "Departamentos"
        ordering = ["dp"]

    def __str__(self):
        return f"{self.dp:02d}"


class Ds(models.Model):
    id = models.AutoField(primary_key=True)
    # dp = models.ForeignKey(Dp, db_column="dp", on_delete=models.PROTECT)
    dp = models.ForeignKey(Dp, on_delete=models.PROTECT)
    ds = models.IntegerField()
    nombre = models.CharField(max_length=50, verbose_name="nombre distrito")

    @cached_property
    def distrito(self):
        return f"{self.ds:02d}"

    class Meta:
        verbose_name_plural = "distritos"
        ordering = ["dp", "ds"]

    def __str__(self):
        return f"{self.ds:02d}"


class Sd(models.Model):
    id = models.AutoField(primary_key=True)
    ds = models.ForeignKey(Ds, db_column="ds", on_delete=models.PROTECT)
    sd = models.IntegerField()
    nombre = models.CharField("nombre subdistrito", max_length=50, blank=True)

    @cached_property
    def subdistrito(self):
        return f"{self.sd:02d}"

    @cached_property
    def dp(self):
        return self.ds.dp

    @cached_property
    def dp_nombre(self):
        return self.ds.dp.nombre

    @cached_property
    def ds_nombre(self):
        return self.ds.nombre

    class Meta:
        verbose_name_plural = "subdistritos"
        ordering = ["ds", "sd"]

    @cached_property
    def completo(self):
        return f"{self.ds.dp}{self.ds}{self.sd:02d}"

    def __str__(self):
        return self.completo

    nomenclatura = property(__str__)


class Lugar(models.Model):
    nombre = models.CharField(max_length=80)
    observacion = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "lugares"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Titulo(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Profesional(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    titulo = models.ForeignKey(Titulo, blank=True, null=True, on_delete=models.SET_NULL)
    icopa = models.CharField("ICoPA", max_length=8, blank=True)
    domicilio = models.CharField(max_length=50, blank=True)
    lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.SET_NULL)
    telefono = models.CharField("teléfono", max_length=15, blank=True)
    web = models.URLField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    cuit_cuil = models.CharField("CUIT/CUIL", max_length=14, unique=True, blank=True, null=True)
    habilitado = models.BooleanField(default=True)
    jubilado = models.BooleanField(default=False)
    fallecido = models.BooleanField(default=False)

    # def get_absolute_url(self):
    #     return reverse("profesional", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "profesionales"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return self.nombre_completo

    @cached_property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres}".strip()

    def save(self, *args, **kwargs):
        self.apellidos = self.apellidos.upper().strip()
        self.nombres = capitalize_phrase(self.nombres)
        super().save(*args, **kwargs)


class Expediente(TimeStampedModel):
    id = models.IntegerField("Expediente", primary_key=True)
    fecha_medicion = models.DateField("Medición", blank=True, null=True)
    inscripcion_numero = models.IntegerField("SCIT Nº", unique=True, blank=True, null=True)
    inscripcion_fecha = models.DateField("SCIT fecha", blank=True, null=True)
    duplicado = models.BooleanField(default=False)
    # certificado_catastral = models.PositiveIntegerField("CC Nº", blank=True, null=True)
    orden_numero = models.IntegerField("CoPA Nº", blank=True, null=True)
    orden_fecha = models.DateField("CoPA fecha", blank=True, null=True)
    sin_inscripcion = models.BooleanField("No se registra", default=False)
    cancelado = models.BooleanField(default=False)
    cancelado_por = models.CharField(max_length=100, blank=True)
    plano_ruta = models.URLField(max_length=100, blank=True)
    objetos = models.ManyToManyField(Objeto)
    profesionales_firmantes = models.ManyToManyField(Profesional)
    personas = models.ManyToManyField("Persona", through="ExpedientePersona", blank=True)
    lugares = models.ManyToManyField("Lugar", through="ExpedienteLugar", blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse("expediente", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("expediente_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("expediente_delete", kwargs={"pk": self.pk})

    def get_update_plano_url(self):
        return reverse("expediente_update_plano", kwargs={"pk": self.pk})

    @cached_property
    def pendiente(self):
        return (not self.inscripcion_numero and not self.cancelado and not self.sin_inscripcion)

    @cached_property
    def propietarios_count(self):
        """Devuelve la cantidad de personas que figuran como propietarias."""
        return self.expedientepersona_set.filter(propietario=True).count()

    def propietarios(self):
        """Devuelve las personas que figuran como propietarias."""
        return self.expedientepersona_set.filter(propietario=True)

    @cached_property
    def firmantes_count(self):
        """
        Devuelve la cantidad de personas que deben firmar la Solicitud de Inscripción.
        """
        return self.firmantes().count()

    def firmantes(self):
        """Devuelve las personas que deben firmar la Solicitud de Inscripción."""
        return self.expedientepersona_set.filter(Q(propietario=True) | Q(sucesor=True)).exclude(sucesion=True)

    @cached_property
    def comitentes_count(self):
        """Devuelve la cantidad de personas que figuran como comitentes."""
        return self.expedientepersona_set.filter(comitente=True).count()

    def comitentes(self):
        """Devuelve las personas que figuran como comitentes."""
        return self.expedientepersona_set.filter(comitente=True)

    @cached_property
    def partidas_count(self):
        """Devuelve la cantidad de partidas vinculadas."""
        return self.expedientepartida_set.count()

    @cached_property
    def partidas_list(self):
        """Devuelve la list() de las partidas vinculadas."""
        return [ep.partida for ep in self.expedientepartida_set.all()]

    @cached_property
    def partidas_str(self):
        """Devuelve la lista de partidas vinculadas separadas por ", "."""
        return ", ".join([p.para_caratula for p in self.partidas_list])

    @cached_property
    def lugares_list(self):
        """Devuelve la list() de los lugares."""
        return [el.lugar.nombre for el in self.expedientelugar_set.all()]

    @cached_property
    def lugares_str(self):
        """Devuelve la lista de lugares separados por ", "."""
        return ", ".join(self.lugares_list)


class ExpedienteLugar(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "lugar"
        verbose_name_plural = "lugares"
        ordering = ["expediente", "lugar"]

    def __str__(self):
        return f"{self.expediente}-{self.lugar.nombre}"

    def get_absolute_url(self):
        return reverse("expedientelugar", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("expedientelugar_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("expedientelugar_delete", kwargs={"pk": self.pk})

    @cached_property
    def catastros_locales_list(self):
        return [cl for cl in self.catastrolocal_set.all()]

    @cached_property
    def catastros_locales_str(self):
        return ", ".join([cl.__str__() for cl in self.catastros_locales_list])


class ExpedientePartida(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    partida = models.ForeignKey("Partida", on_delete=models.CASCADE)
    set_ruta = models.URLField(max_length=100, blank=True)
    # informe_catastral = FileBrowseField(
    #     max_length=200,
    #     directory="set/",
    #     extensions=[".pdf"],
    # )

    class Meta:
        unique_together = ["expediente", "partida"]
        verbose_name = "partida"
        verbose_name_plural = "partidas"
        ordering = ["expediente", "partida"]

    def __str__(self):
        return f"{self.partida}"

    def get_update_url(self):
        return reverse(
            "partida_to_expediente", kwargs={"expediente_id": self.expediente.pk, "partida_id": self.partida.pk}
        )

    def get_delete_url(self):
        return reverse("expedientepartida_delete", kwargs={"pk": self.pk})


class ExpedientePersona(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    persona = models.ForeignKey("Persona", on_delete=models.CASCADE)
    comitente = models.BooleanField(default=False)
    propietario = models.BooleanField(default=True)
    poseedor = models.BooleanField(default=False)
    sucesor = models.BooleanField(default=False)
    partes_indivisas_propias = models.IntegerField(blank=True)
    partes_indivisas_total = models.IntegerField(blank=True)
    sucesion = models.BooleanField("sucesión", default=False)
    nuda_propiedad = models.BooleanField("nuda prop", default=False)
    usufructo = models.BooleanField("usuf", default=False)

    class Meta:
        unique_together = ["expediente", "persona"]
        verbose_name = "persona involucrada"
        verbose_name_plural = "personas involucradas"
        ordering = ["expediente", "persona__apellidos", "persona__nombres"]

    def __str__(self):
        return f"{self.expediente.id} - {self.persona.apellidos} {self.persona.nombres}"

    def get_update_url(self):
        return reverse(
            "persona_to_expediente", kwargs={"expediente_id": self.expediente.pk, "persona_id": self.persona.pk}
        )

    def get_delete_url(self):
        return reverse("expedientepersona_delete", kwargs={"pk": self.pk})


class Partida(models.Model):
    sd = models.ForeignKey("SD", db_column="sd", blank=True, null=True, default=None, on_delete=models.SET_NULL)
    pii = models.IntegerField("partida")
    subpii = models.IntegerField("subpartida", default=0)

    class Meta:
        unique_together = ("sd", "pii", "subpii")
        ordering = ["pii", "subpii"]

    def __str__(self):
        return self.partida

    # def get_absolute_url(self):
    #     return reverse("partida", kwargs={"pk": self.pk})

    # def get_update_url(self, eid=None):
    #     if eid:
    #         return reverse("partida_update", kwargs={"pk": self.pk, "eid": eid})
    #     else:
    #         return reverse("partida_update", kwargs={"pk": self.pk})

    # def get_delete_url(self):
    #     return reverse("partida_delete", kwargs={"pk": self.pk})

    @cached_property
    def partida(self):
        return f"{self.pii:06d}/{self.subpii:04d}"

    @cached_property
    def partida_completa(self):
        return f"{self.sd}-{self.partida}" if self.sd else self.partida

    @cached_property
    def partida_api(self):
        return f"{self.sd}-{self.partida}-{self.api}" if self.sd else self.partida

    @cached_property
    def para_caratula(self):
        return f"{self.sd.dp}-{self.sd.ds}-{self.sd.sd:02d} {self.partida}" if self.sd else self.partida

    def get_dvapi(self):
        coef = "9731"
        _coef = coef + coef + coef + coef
        sd = int(self.sd.completo)
        strpii = f"{sd or 0:06d}{self.pii or 0:06d}{self.subpii or 0:04d}"
        suma = 0
        for i in range(0, len(strpii)):
            m = str(int(strpii[i]) * int(_coef[i]))
            suma += int(m[len(m) - 1])
        return (10 - (suma % 10)) % 10

    # def get_dvapi(self):
    #     if self.sd:
    #         return self.calc_dvapi(int(self.sd.nomenclatura), self.pii, self.subpii)
    #     return None

    api = property(get_dvapi)


class PartidaDominio(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    tomo = models.IntegerField(blank=True)
    par = models.BooleanField(default=False)
    impar = models.BooleanField(default=False)
    folio = models.IntegerField(blank=True)
    numero = models.IntegerField(blank=True)
    fecha = models.DateField(blank=True)
    fecha_inscripcion_definitiva = models.DateField(blank=True)

    class Meta:
        verbose_name_plural = "partida_dominios"


class Persona(models.Model):
    nombres = models.CharField("nombre", max_length=100, blank=True)
    apellidos = models.CharField("apellido", max_length=100)
    nombres_alternativos = models.CharField(max_length=100, blank=True)
    apellidos_alternativos = models.CharField(max_length=100, blank=True)
    domicilio = models.CharField(max_length=50, blank=True)
    lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.SET_NULL)
    telefono = models.CharField("teléfono", max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    cuit_cuil = models.CharField("CUIT/CUIL/CDI", max_length=14, unique=True, blank=True, null=True)
    TIPO_DOC = ((0, "DNI"), (1, "LC"), (2, "LE"), (3, "Otro"), (4, "Extranjero"))
    tipo_doc = models.SmallIntegerField("tipo documento", choices=TIPO_DOC, blank=True, null=True, default=None)
    documento = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        unique_together = ("tipo_doc", "documento")

    def __str__(self):
        return self.nombre_completo

    def get_absolute_url(self):
        return reverse("persona", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("persona_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("persona_delete", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.apellidos = self.apellidos.upper().strip()
        self.apellidos_alternativos = self.apellidos_alternativos.upper().strip()
        self.nombres = capitalize_phrase(self.nombres)
        self.nombres_alternativos = capitalize_phrase(self.nombres_alternativos)
        super().save(*args, **kwargs)

    @cached_property
    def nombre_completo(self):
        return f"{self.apellidos} {self.nombres or ''}".strip()

    @cached_property
    def nombre_completo_elipsis(self):
        return self.nombre_completo if len(self.nombre_completo) < 30 else f"{self.nombre_completo[:30]}&mldr;"

    @cached_property
    def nombre_alternativo(self):
        if self.apellidos_alternativos or self.nombres_alternativos:
            return (
                f"{self.apellidos_alternativos or self.apellidos} {self.nombres_alternativos or self.nombres}".strip()
            )

    @cached_property
    def domicilio_completo(self):
        localidad = f", {self.lugar}" if self.lugar and self.domicilio else self.lugar or ""
        return f"{self.domicilio}{localidad}".strip() if self.domicilio else localidad

    @cached_property
    def documento_completo(self):
        if self.documento:
            return f"{self.get_tipo_doc_display()} {self.documento}".strip()
        else:
            return ""

    @cached_property
    def cuit_link(self):
        url = '<a href="http://www.cuitonline.com/search.php?q=%s">%s</a>'
        if self.cuit_cuil:
            return mark_safe(url % (self.cuit_cuil, self.cuit_cuil))
        elif self.documento:
            return mark_safe(url % (self.documento, "buscar"))
        elif self.apellidos:
            return mark_safe(url % (self.nombre_completo, "buscar"))
        else:
            return ""


class Zona(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}"
