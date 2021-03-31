# Generated by Django 3.1.7 on 2021-03-26 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0009_expediente_personas'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='lugares',
            field=models.ManyToManyField(blank=True, through='gea.ExpedienteLugar', to='gea.Lugar'),
        ),
    ]
