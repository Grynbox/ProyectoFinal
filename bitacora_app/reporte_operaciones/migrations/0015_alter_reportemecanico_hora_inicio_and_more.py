# Generated by Django 5.0.8 on 2024-10-31 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0014_remove_reportemecanico_hora_suspendido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportemecanico',
            name='hora_inicio',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='reportemecanico',
            name='hora_termiando',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]
