# Generated by Django 3.1.7 on 2021-03-31 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0010_expediente_lugares'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expedientepersona',
            options={'ordering': ['expediente', 'persona__apellidos', 'persona__nombres'], 'verbose_name': 'persona involucrada', 'verbose_name_plural': 'personas involucradas'},
        ),
    ]
