# Generated by Django 5.0.8 on 2024-09-23 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0002_rename_ano_unidad_vehiculos_año_unidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporteentrada',
            name='fecha_terminado',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]