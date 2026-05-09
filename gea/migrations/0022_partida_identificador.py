from django.db import migrations, models


def backfill_identificador(apps, schema_editor):
    Partida = apps.get_model("gea", "Partida")
    coef = "9731" * 4

    # Partidas SIN sd
    batch = []
    for p in Partida.objects.filter(sd__isnull=True).iterator(chunk_size=500):
        p.identificador = f"{p.pii:06d}/{p.subpii:04d}"
        batch.append(p)
        if len(batch) >= 500:
            Partida.objects.bulk_update(batch, ["identificador"])
            batch = []
    if batch:
        Partida.objects.bulk_update(batch, ["identificador"])

    # Partidas CON sd
    batch = []
    for p in (
        Partida.objects.filter(sd__isnull=False)
        .select_related("sd__ds__dp")
        .iterator(chunk_size=500)
    ):
        dp_num, ds_num, sd_num = p.sd.ds.dp.dp, p.sd.ds.ds, p.sd.sd
        strpii = f"{dp_num:02d}{ds_num:02d}{sd_num:02d}{p.pii:06d}{p.subpii:04d}"
        suma = sum(int(str(int(strpii[i]) * int(coef[i]))[-1]) for i in range(len(strpii)))
        dv = (10 - (suma % 10)) % 10
        p.identificador = f"{dp_num:02d}-{ds_num:02d}-{sd_num:02d} {p.pii:06d}/{p.subpii:04d}-{dv}"
        batch.append(p)
        if len(batch) >= 500:
            Partida.objects.bulk_update(batch, ["identificador"])
            batch = []
    if batch:
        Partida.objects.bulk_update(batch, ["identificador"])


def clear_identificador(apps, schema_editor):
    apps.get_model("gea", "Partida").objects.all().update(identificador="")


class Migration(migrations.Migration):

    dependencies = [
        ("gea", "0021_alter_ds_ds_alter_expedientepersona_nuda_propiedad_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="partida",
            name="identificador",
            field=models.CharField(blank=True, db_index=True, default="", editable=False, max_length=30),
        ),
        migrations.RunPython(backfill_identificador, reverse_code=clear_identificador),
    ]
