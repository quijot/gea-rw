# Generated by Django 3.1.7 on 2021-04-02 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0012_remove_expediente_fecha_plano'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesional',
            name='cuit_cuil',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='CUIT/CUIL'),
        ),
        migrations.AlterField(
            model_name='profesional',
            name='lugar',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gea.lugar'),
        ),
    ]