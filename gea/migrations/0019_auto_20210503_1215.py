# Generated by Django 3.2 on 2021-05-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gea', '0018_auto_20210426_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedientepersona',
            name='sucesion',
            field=models.BooleanField(default=False, verbose_name='sucesión'),
        ),
        migrations.AlterUniqueTogether(
            name='expedientepersona',
            unique_together={('expediente', 'persona')},
        ),
    ]
